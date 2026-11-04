from code2prompt.utils.is_binary import detect_utf16_encoding, is_binary


import os
import tempfile
from pathlib import Path


def _write_temp(data):
    temp_file = tempfile.NamedTemporaryFile(mode='wb', delete=False)
    temp_file.write(data)
    temp_file.close()
    return Path(temp_file.name)


def test_is_binary():
    with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', delete=False) as temp_file:
        temp_file.write("Text content")
        temp_file.flush()
        assert not is_binary(Path(temp_file.name))
    os.unlink(temp_file.name)

    with tempfile.NamedTemporaryFile(mode='wb', delete=False) as temp_file:
        temp_file.write(b"\x00\x01\x02")
        temp_file.flush()
        assert is_binary(Path(temp_file.name))
    os.unlink(temp_file.name)


def test_utf16_text_is_not_binary():
    # The exact reproduction from the issue: UTF-16 (BOM) HTML output.
    sample = "<!DOCTYPE html>\r\n<html>\r\n<body>\r\n<p>Hello World</p>\r\n</body>\r\n</html>\r\n"
    for data in (
        sample.encode("utf-16"),  # BOM, little-endian
        sample.encode("utf-16-be"),  # no BOM, big-endian
        sample.encode("utf-16-le"),  # no BOM, little-endian
    ):
        path = _write_temp(data)
        try:
            assert not is_binary(path)
        finally:
            os.unlink(path)


def test_binary_with_nul_bytes_stays_binary():
    for data in (
        b"\x00\x01\x02",
        b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR",
        bytes(range(256)),
    ):
        path = _write_temp(data)
        try:
            assert is_binary(path)
        finally:
            os.unlink(path)


def test_detect_utf16_encoding():
    assert detect_utf16_encoding("hello".encode("utf-16")) == "utf-16"
    assert detect_utf16_encoding("hello".encode("utf-16-le")) == "utf-16-le"
    assert detect_utf16_encoding("hello".encode("utf-16-be")) == "utf-16-be"
    assert detect_utf16_encoding(b"plain ascii") is None
    assert detect_utf16_encoding(b"\x00\x01\x02") is None