import pytest
from click.testing import CliRunner
from code2prompt.main import create_markdown_file
from code2prompt.utils.analyzer import analyze_codebase, format_flat_output, format_tree_output, get_extension_list
from pathlib import Path
import tempfile
import os

@pytest.fixture
def temp_codebase():
    with tempfile.TemporaryDirectory() as tmpdirname:
        # Create a temporary codebase structure
        Path(tmpdirname, "file1.py").touch()
        Path(tmpdirname, "file2.js").touch()
        Path(tmpdirname, "subfolder").mkdir()
        Path(tmpdirname, "subfolder", "file3.py").touch()
        Path(tmpdirname, "subfolder", "file4.css").touch()
        yield tmpdirname

def test_analyze_codebase(temp_codebase):
    extension_counts, extension_dirs = analyze_codebase(temp_codebase)
    assert extension_counts == {".py": 2, ".js": 1, ".css": 1}
    assert len(extension_dirs) == 3
    assert len(extension_dirs[".py"]) == 2  # .py files in root and subfolder
    assert len(extension_dirs[".js"]) == 1
    assert len(extension_dirs[".css"]) == 1

def test_format_flat_output():
    extension_counts = {".py": 2, ".js": 1, ".css": 1}
    output = format_flat_output(extension_counts)
    assert ".py: 2 files" in output
    assert ".js: 1 file" in output
    assert ".css: 1 file" in output

#def test_format_tree_output(temp_codebase):
#    _, extension_dirs = analyze_codebase(temp_codebase)
#    output = format_tree_output(extension_dirs)
#    assert "└── .py" in output
#    assert "└── .js" in output
#    assert "└── .css" in output
#    assert "subfolder" in output

def test_get_extension_list():
    extension_counts = {".py": 2, ".js": 1, ".css": 1}
    extension_list = get_extension_list(extension_counts)
    assert extension_list == ".css,.js,.py"

def test_analyze_command_flat(temp_codebase):
    runner = CliRunner()
    result = runner.invoke(create_markdown_file, ['--analyze', '-p', temp_codebase])
    assert result.exit_code == 0
    assert ".py: 2 files" in result.output
    assert ".js: 1 file" in result.output
    assert ".css: 1 file" in result.output
    assert "Comma-separated list of extensions:" in result.output
    assert ".css,.js,.py" in result.output

#def test_analyze_command_tree(temp_codebase):
#    runner = CliRunner()
#    result = runner.invoke(create_markdown_file, ['--analyze', '-p', temp_codebase, '--format', 'tree'])
#    assert result.exit_code == 0
#    assert "└── .py" in result.output
#    assert "└── .js" in result.output
#    assert "└── .css" in result.output
#    assert "subfolder" in result.output
#    assert "Comma-separated list of extensions:" in result.output
#    assert ".css,.js,.py" in result.output

#def test_analyze_command_multiple_paths(temp_codebase):
#    runner = CliRunner()
#    with tempfile.TemporaryDirectory() as second_codebase:
#        Path(second_codebase, "file5.java").touch()
#        result = runner.invoke(create_markdown_file, ['--analyze', '-p', temp_codebase, '-p', second_codebase])
#        assert result.exit_code == 0
#        assert ".py: 2 files" in result.output
#        assert ".js: 1 file" in result.output
#        assert ".css: 1 file" in result.output
#        assert ".java: 1 file" in result.output
#        assert "Comma-separated list of extensions:" in result.output
#        assert ".css,.java,.js,.py" in result.output

def test_analyze_command_empty_directory():
    runner = CliRunner()
    with tempfile.TemporaryDirectory() as empty_dir:
        result = runner.invoke(create_markdown_file, ['--analyze', '-p', empty_dir])
        assert result.exit_code == 0
        assert "No files found" in result.output or result.output.strip() == ""

def test_analyze_command_nonexistent_directory():
    runner = CliRunner()
    result = runner.invoke(create_markdown_file, ['--analyze', '-p', '/nonexistent/directory'])
    assert result.exit_code != 0
    assert "Error" in result.output or "does not exist" in result.output