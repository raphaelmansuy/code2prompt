import os
import tempfile
from pathlib import Path

from code2prompt.core.process_file import process_file

SAMPLE = "<!DOCTYPE html>\r\n<html>\r\n<body>\r\n<p>Hello World</p>\r\n</body>\r\n</html>\r\n"


def _write_temp(data):
    temp_file = tempfile.NamedTemporaryFile(mode="wb", delete=False, suffix=".htm")
    temp_file.write(data)
    temp_file.close()
    return Path(temp_file.name)


def test_process_file_reads_utf16():
    # Issue #30 reproduction: UTF-16LE with BOM must yield its text content.
    for encoding in ("utf-16", "utf-16-le", "utf-16-be"):
        path = _write_temp(SAMPLE.encode(encoding))
        try:
            result = process_file(path, False, False, False, {})
            assert result is not None
            assert "Hello World" in result["content"]
            assert "\x00" not in result["content"]
        finally:
            os.unlink(path)


def test_process_file_returns_none_for_binary():
    path = _write_temp(bytes(range(256)))
    try:
        assert process_file(path, False, False, False, {}) is None
    finally:
        os.unlink(path)
