from code2prompt.utils.parse_gitignore import parse_gitignore


import os
import tempfile
from pathlib import Path


def test_parse_gitignore():
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as temp_file:
        temp_file.write("*.pyc\n# Comment\n/dist/\n")
        temp_file.flush()
        gitignore_path = Path(temp_file.name)

    patterns = parse_gitignore(gitignore_path)
    assert patterns == {"*.pyc", "/dist/"}

    os.unlink(temp_file.name)