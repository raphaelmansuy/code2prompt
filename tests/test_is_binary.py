from code2prompt.utils.is_binary import is_binary


import os
import tempfile
from pathlib import Path


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