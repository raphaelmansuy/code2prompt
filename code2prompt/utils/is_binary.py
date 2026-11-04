"""Binary-file detection, with an exception for UTF-16 text.

UTF-16 text (a common default for Windows/PowerShell and Microsoft tool
output) interleaves ASCII characters with NUL bytes, so the naive
"contains a NUL byte" check misclassifies it as binary and code2prompt
silently drops the file. This module treats a file as UTF-16 text when
it carries a UTF-16 byte-order mark, or when its leading bytes decode
as UTF-16 whose code units are overwhelmingly ASCII text (a NUL in the
high-byte position plus a printable low byte). Anything else containing
a NUL byte is still binary.
"""


def _is_ascii_text_unit(high_byte, low_byte):
    """One UTF-16 code unit of plain ASCII text: NUL high byte, printable low."""
    return high_byte == 0x00 and (low_byte in (0x09, 0x0A, 0x0D) or 0x20 <= low_byte <= 0x7E)


def detect_utf16_encoding(chunk):
    """Return a codec name for UTF-16 text in ``chunk``, or ``None``.

    ``"utf-16"`` (BOM-aware) is returned for byte-order-marked data;
    otherwise ``"utf-16-le"`` / ``"utf-16-be"`` when at least 80% of the
    complete code units look like ASCII text. Files in non-Latin scripts
    without a BOM are not detected by this heuristic and keep the old
    behaviour; BOM-marked files of any script are detected.
    """
    if chunk.startswith(b"\xff\xfe") or chunk.startswith(b"\xfe\xff"):
        return "utf-16"
    if b"\x00" not in chunk:
        return None
    usable = chunk[: len(chunk) - len(chunk) % 2]
    if len(usable) < 2:
        return None
    for encoding, high_index in (("utf-16-le", 1), ("utf-16-be", 0)):
        units = [usable[i : i + 2] for i in range(0, len(usable), 2)]
        text_like = sum(
            1
            for unit in units
            if _is_ascii_text_unit(unit[high_index], unit[1 - high_index])
        )
        if units and text_like / len(units) >= 0.8:
            return encoding
    return None


def is_binary(file_path):
    try:
        with open(file_path, "rb") as file:
            chunk = file.read(1024)
            if b"\x00" not in chunk:
                return False
            return detect_utf16_encoding(chunk) is None
    except IOError:
        print(f"Error: The file at {file_path} could not be opened.")
        return False
