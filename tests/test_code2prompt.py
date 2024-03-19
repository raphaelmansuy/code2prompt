import os
import tempfile
from pathlib import Path
from click.testing import CliRunner
from code2prompt.main import create_markdown_file, parse_gitignore, is_ignored, is_filtered, is_binary

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

def test_is_filtered():
    assert is_filtered(Path("file.py"), "*.py")
    assert not is_filtered(Path("file.txt"), "*.py")
    
    
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