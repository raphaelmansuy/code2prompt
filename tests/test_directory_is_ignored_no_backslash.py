from code2prompt.utils.is_ignored import is_ignored


from pathlib import Path


def test_directory_is_ignored_no_backslash():
    gitignore_patterns = ["*.pyc", "/dist", ".git", ".venv"]
    base_path = Path("/project")

    assert is_ignored(Path("/project/.venv/bin/python"), gitignore_patterns, base_path)
    assert is_ignored(Path("/project/.venv/lib/site-packages"), gitignore_patterns, base_path)
    assert not is_ignored(Path("/project/file.txt"), gitignore_patterns, base_path)