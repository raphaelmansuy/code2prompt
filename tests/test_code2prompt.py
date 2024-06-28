import os
import tempfile
from pathlib import Path
from click.testing import CliRunner
from code2prompt.utils.is_binary import is_binary
from code2prompt.utils.is_filtered import is_filtered
from code2prompt.utils.is_ignored import is_ignored
from code2prompt.main import create_markdown_file
from code2prompt.utils.parse_gitignore import parse_gitignore

def test_parse_gitignore():
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as temp_file:
        temp_file.write("*.pyc\n# Comment\n/dist/\n")
        temp_file.flush()
        gitignore_path = Path(temp_file.name)

    patterns = parse_gitignore(gitignore_path)
    assert patterns == {"*.pyc", "/dist/"}

    os.unlink(temp_file.name)

def test_is_ignored():
    gitignore_patterns = ["*.pyc", "/dist/"]
    base_path = Path("/project")

    assert is_ignored(Path("/project/file.pyc"), gitignore_patterns, base_path)
    assert is_ignored(Path("/project/dist/file.txt"), gitignore_patterns, base_path)
    assert not is_ignored(Path("/project/file.txt"), gitignore_patterns, base_path)
    
def test_git_directory_is_ignored():
    gitignore_patterns = ["*.pyc", "/dist/", ".git/"]
    base_path = Path("/project")

    assert is_ignored(Path("/project/.git/config"), gitignore_patterns, base_path)
    assert is_ignored(Path("/project/.git/HEAD"), gitignore_patterns, base_path)
    assert not is_ignored(Path("/project/file.txt"), gitignore_patterns, base_path)    
    
def test_venv_directory_is_ignored():
    gitignore_patterns = ["*.pyc", "/dist/", ".git/", ".venv/"]
    base_path = Path("/project")

    assert is_ignored(Path("/project/.venv/bin/python"), gitignore_patterns, base_path)
    assert is_ignored(Path("/project/.venv/lib/site-packages"), gitignore_patterns, base_path)
    assert not is_ignored(Path("/project/file.txt"), gitignore_patterns, base_path)    
    
def test_directory_is_ignored_no_backslash():
    gitignore_patterns = ["*.pyc", "/dist", ".git", ".venv"]
    base_path = Path("/project")

    assert is_ignored(Path("/project/.venv/bin/python"), gitignore_patterns, base_path)
    assert is_ignored(Path("/project/.venv/lib/site-packages"), gitignore_patterns, base_path)
    assert not is_ignored(Path("/project/file.txt"), gitignore_patterns, base_path)      
    

def test_relative_path_is_ignored():
    gitignore_patterns = ["*.pyc", "/dist/", ".git/", ".venv/", "relative_dir/"]
    base_path = Path("/project")

    assert is_ignored(Path("/project/relative_dir/file.txt"), gitignore_patterns, base_path)
    assert not is_ignored(Path("/project/other_dir/file.txt"), gitignore_patterns, base_path)    

def test_nested_path_is_ignored():
    gitignore_patterns = ["*.pyc", "/dist/", ".git/", ".venv/", "relative_dir/", "nested_dir/*/*"]
    base_path = Path("/project")

    assert is_ignored(Path("/project/nested_dir/sub_dir/file.txt"), gitignore_patterns, base_path)
    assert not is_ignored(Path("/project/nested_dir/file.txt"), gitignore_patterns, base_path)
    assert not is_ignored(Path("/project/other_dir/file.txt"), gitignore_patterns, base_path)    


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




def test_create_markdown_file():
    runner = CliRunner()

    with tempfile.TemporaryDirectory() as temp_dir:
        temp_dir_path = Path(temp_dir)
        (temp_dir_path / "file1.py").write_text("print('Hello')")
        (temp_dir_path / "file2.txt").write_text("Text content")
        (temp_dir_path / ".gitignore").write_text("*.txt")

        result = runner.invoke(create_markdown_file, ['-p', temp_dir])
        assert result.exit_code == 0
        assert "file1.py" in result.output
        assert "file2.txt" not in result.output

        output_file = temp_dir_path / "output.md"
        result = runner.invoke(create_markdown_file, ['-p', temp_dir, '-o', str(output_file)])
        assert result.exit_code == 0
        assert output_file.exists()
        assert "file1.py" in output_file.read_text()
        assert "file2.txt" not in output_file.read_text()
        
        
def test_create_markdown_with_filter():
    runner = CliRunner()
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_dir_path = Path(temp_dir)
        (temp_dir_path / "file1.py").write_text("print('Hello')")
        (temp_dir_path / "file2.py").write_text("print('World')")
        (temp_dir_path / "file3.txt").write_text("Text content")
        (temp_dir_path / ".gitignore").write_text("*.txt")

        filter_option = "*.py"
        output_file = temp_dir_path / "output_with_filter.md"
        result = runner.invoke(create_markdown_file, ['-p', temp_dir, '-o', str(output_file), '-f', filter_option])
        
        assert result.exit_code == 0
        assert output_file.exists()
        output_content = output_file.read_text()
        assert "file1.py" in output_content
        assert "file2.py" in output_content
        assert "file3.txt" not in output_content  # Ensuring .txt files are filtered out
        
        
def test_create_markdown_with_exclude():
    runner = CliRunner()
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_dir_path = Path(temp_dir)
        (temp_dir_path / "file1.py").write_text("print('Hello')")
        (temp_dir_path / "file2.py").write_text("print('World')")
        (temp_dir_path / "file3.txt").write_text("Text content")
        (temp_dir_path / "ignore_me.py").write_text("# This should be ignored")

        exclude_option = "ignore_me.py"
        output_file = temp_dir_path / "output_with_exclude.md"
        result = runner.invoke(create_markdown_file, ['-p', temp_dir, '-o', str(output_file), '-e', exclude_option])
        
        assert result.exit_code == 0
        assert output_file.exists()
        output_content = output_file.read_text()
        assert "file1.py" in output_content
        assert "file2.py" in output_content
        assert "file3.txt" in output_content  # Assuming we want to include non-Python files by default
        assert "ignore_me.py" not in output_content  # Ensuring excluded file is not in the output
        
        
def test_add_line_numbers():
    # Sample content to test
    content = """First line
Second line
Third line"""

    # Expected output with line numbers added
    expected_output = """1: First line
2: Second line
3: Third line"""

    # Function to add line numbers
    def add_line_numbers(content):
        lines = content.split('\n')
        numbered_lines = [f"{i + 1}: {line}" for i, line in enumerate(lines)]
        return '\n'.join(numbered_lines)

    # Actual output from the function
    actual_output = add_line_numbers(content)

    # Assert that the actual output matches the expected output
    assert actual_output == expected_output, "Line numbers were not added correctly."        