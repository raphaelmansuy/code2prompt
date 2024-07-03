from code2prompt.utils.is_ignored import is_ignored


from pathlib import Path


def test_git_directory_is_ignored():
    gitignore_patterns = ["*.pyc", "/dist/", ".git/"]
    base_path = Path("/project")

    assert is_ignored(Path("/project/.git/config"), gitignore_patterns, base_path)
    assert is_ignored(Path("/project/.git/HEAD"), gitignore_patterns, base_path)
    assert not is_ignored(Path("/project/file.txt"), gitignore_patterns, base_path)