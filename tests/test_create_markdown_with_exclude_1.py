from code2prompt.main import create_markdown_file


from click.testing import CliRunner


import tempfile
from pathlib import Path


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