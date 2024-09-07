import pytest
from pathlib import Path
from code2prompt.utils.is_filtered import is_filtered


@pytest.mark.parametrize(
    "file_path, include_pattern, exclude_pattern, case_sensitive, expected",
    [
        (Path("file.txt"), "", "", False, True),
        (Path("file.py"), "*.py", "", False, True),
        (Path("file.txt"), "*.py", "", False, False),
        (Path("file.py"), "", "*.py", False, False),
        (Path("file.txt"), "", "*.py", False, True),
        (Path("file.py"), "*.py,*.txt", "test_*.py", False, True),
        (Path("test_file.py"), "*.py,*.txt", "test_*.py", False, False),
        (Path("File.PY"), "*.py", "", True, False),
        (Path("File.PY"), "*.py", "", False, True),
        #    (Path("test/file.py"), "**/test/*.py", "", False, True),
        (Path("src/file.py"), "**/test/*.py", "", False, False),
        (Path("file.txt"), "*.py,*.js,*.txt", "", False, True),
        (Path("file.md"), "*.py,*.js,*.txt", "", False, False),
        (Path("test_file.py"), "*.py", "test_*.py", False, False),
        (Path(".hidden_file"), "*", "", False, True),
        (Path("file_without_extension"), "", "*.*", False, True),
        (Path("deeply/nested/directory/file.txt"), "**/*.txt", "", False, True),
        (Path("file.txt.bak"), "", "*.bak", False, False),
    ],
)
def test_is_filtered(
    file_path, include_pattern, exclude_pattern, case_sensitive, expected
):
    assert (
        is_filtered(file_path, include_pattern, exclude_pattern, case_sensitive)
        == expected
    )


def test_is_filtered_with_directories():
    assert is_filtered(
        Path("src/test"), "**/test", "", False
    )  # Removed comparison to True
    assert not is_filtered(Path("src/prod"), "**/test", "", False)  # Updated to use not


def test_is_filtered_empty_patterns():
    assert is_filtered(Path("any_file.txt"))  # Removed comparison to True


def test_is_filtered_case_sensitivity():
    assert not is_filtered(Path("File.TXT"), "*.txt", "", True)  # Updated comparison
    assert is_filtered(Path("File.TXT"), "*.txt", "", False)  # Unchanged


def test_is_filtered_exclude_precedence():
    assert not is_filtered(Path("important_test.py"), "*.py", "*test*", False)
