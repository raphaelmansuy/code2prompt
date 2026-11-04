"""
This module contains the function to process a file and extract its metadata and content.
"""

from pathlib import Path
from datetime import datetime

from code2prompt.utils.add_line_numbers import add_line_numbers
from code2prompt.utils.is_binary import detect_utf16_encoding
from code2prompt.utils.language_inference import infer_language
from code2prompt.comment_stripper.strip_comments import strip_comments


def process_file(
    file_path: Path, suppress_comments: bool, line_number: bool, no_codeblock: bool, syntax_map: dict
):
    """
    Processes a given file to extract its metadata and content.

    Parameters:
    - file_path (Path): The path to the file to be processed.
    - suppress_comments (bool): Flag indicating whether to remove comments from the file content.
    - line_number (bool): Flag indicating whether to add line numbers to the file content.
    - no_codeblock (bool): Flag indicating whether to disable wrapping code inside markdown code blocks.
    - syntax_map (dict): Custom syntax mappings for language inference.

    Returns:
    dict: A dictionary containing the file information and content.
    """
    file_extension = file_path.suffix
    file_size = file_path.stat().st_size
    file_creation_time = datetime.fromtimestamp(file_path.stat().st_ctime).strftime(
        "%Y-%m-%d %H:%M:%S"
    )
    file_modification_time = datetime.fromtimestamp(file_path.stat().st_mtime).strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    try:
        with file_path.open("r", encoding="utf-8") as f:
            file_content = f.read()
        if "\x00" in file_content:
            # UTF-16 bytes decode as "valid" UTF-8 with embedded NULs, so a
            # NUL here means this is not plain UTF-8 text after all.
            raise UnicodeDecodeError("utf-8", b"", 0, 1, "NUL byte in text")
    except UnicodeDecodeError:
        # UTF-8 failed: fall back to UTF-16 when the bytes look like
        # UTF-16 text (see is_binary.detect_utf16_encoding). Otherwise the
        # file is genuinely undecodable and is skipped, as before.
        try:
            raw = file_path.read_bytes()
        except OSError:
            return None
        encoding = detect_utf16_encoding(raw[:1024])
        if encoding is None:
            return None
        try:
            file_content = raw.decode(encoding)
        except UnicodeDecodeError:
            return None

    try:
        language = infer_language(file_path.name, syntax_map)

        if suppress_comments and language != "unknown":
            file_content = strip_comments(file_content, language)

        if line_number:
            file_content = add_line_numbers(file_content)
    except UnicodeDecodeError:
        return None

    return {
        "path": str(file_path),
        "extension": file_extension,
        "language": language,
        "size": file_size,
        "created": file_creation_time,
        "modified": file_modification_time,
        "content": file_content,
        "no_codeblock": no_codeblock,
    }
