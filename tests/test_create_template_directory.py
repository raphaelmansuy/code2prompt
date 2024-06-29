import pytest
import os
from pathlib import Path
from code2prompt.utils.create_template_directory import create_templates_directory


@pytest.fixture
def temp_dir(tmp_path):
    """Fixture to provide a temporary directory for testing."""
    original_cwd = Path.cwd()
    os.chdir(tmp_path)
    yield tmp_path
    os.chdir(original_cwd)

def test_create_templates_directory_existing(temp_dir, monkeypatch):
    # Create the templates directory beforehand
    templates_dir = temp_dir / "templates"
    templates_dir.mkdir()

    # Mock the print function to capture output
    printed_messages = []
    monkeypatch.setattr('builtins.print', lambda *args: printed_messages.append(' '.join(map(str, args))))

    # Call the function
    create_templates_directory()

    # Verify that the function doesn't raise an exception when the directory already exists
    assert templates_dir.exists()
    assert templates_dir.is_dir()

    # Check if the example template files were created
    expected_files = ["basic.j2", "detailed.j2", "custom.md"]
    for file in expected_files:
        assert (templates_dir / file).exists()
        assert (templates_dir / file).is_file()

    # Verify the printed output
    assert len(printed_messages) == 5
    assert f"Templates directory created at: {templates_dir}" in printed_messages[0]
    assert "Example templates added:" in printed_messages[1]
    for i, file in enumerate(expected_files, start=2):
        assert f"- {file}" in printed_messages[i]