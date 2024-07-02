from code2prompt.utils.is_filtered import is_filtered


from pathlib import Path


def test_is_filtered():
    # Test inclusion patterns
    assert is_filtered(Path("file.py"), "*.py")
    assert not is_filtered(Path("file.txt"), "*.py")

    # Test exclusion patterns
    assert not is_filtered(Path("file.py"), "*.py", "*.py")
    assert is_filtered(Path("file.py"), "*.py", "*.txt")

    # Test case sensitivity
    assert is_filtered(Path("FILE.PY"), "*.py", case_sensitive=False)
    assert not is_filtered(Path("FILE.PY"), "*.py", case_sensitive=True)

    # Test no inclusion pattern (should include all)
    assert is_filtered(Path("file.py"), "", "*.txt")
    assert not is_filtered(Path("file.txt"), "", "*.txt")

    # Test no exclusion pattern (should exclude none)
    assert is_filtered(Path("file.py"), "*.py", "")
    assert is_filtered(Path("file.txt"), "*.txt", "")