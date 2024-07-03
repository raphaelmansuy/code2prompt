from code2prompt.main import create_markdown_file


from click.testing import CliRunner


import tempfile
from pathlib import Path


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