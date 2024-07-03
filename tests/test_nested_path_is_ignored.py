from code2prompt.utils.is_ignored import is_ignored


from pathlib import Path


def test_nested_path_is_ignored():
    gitignore_patterns = ["*.pyc", "/dist/", ".git/", ".venv/", "relative_dir/", "nested_dir/*/*"]
    base_path = Path("/project")

    assert is_ignored(Path("/project/nested_dir/sub_dir/file.txt"), gitignore_patterns, base_path)
    assert not is_ignored(Path("/project/nested_dir/file.txt"), gitignore_patterns, base_path)
    assert not is_ignored(Path("/project/other_dir/file.txt"), gitignore_patterns, base_path)