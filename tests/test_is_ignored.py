from code2prompt.utils.is_ignored import is_ignored


from pathlib import Path


def test_is_ignored():
    gitignore_patterns = ["*.pyc", "/dist/"]
    base_path = Path("/project")

    assert is_ignored(Path("/project/file.pyc"), gitignore_patterns, base_path)
    assert is_ignored(Path("/project/dist/file.txt"), gitignore_patterns, base_path)
    assert not is_ignored(Path("/project/file.txt"), gitignore_patterns, base_path)