import pytest
from pathlib import Path
import tempfile
from unittest.mock import patch
from code2prompt.utils.create_template_directory import create_templates_directory

@pytest.fixture
def temp_dir():
    with tempfile.TemporaryDirectory() as tmpdirname:
        yield Path(tmpdirname)

@pytest.fixture
def mock_package_templates(temp_dir):
    package_templates = temp_dir / "package_templates"
    package_templates.mkdir()
    (package_templates / "template1.j2").write_text("Template 1 content")
    (package_templates / "template2.j2").write_text("Template 2 content")
    return package_templates

def test_create_new_templates(temp_dir, mock_package_templates):
    dest_dir = temp_dir / "dest"
    create_templates_directory(mock_package_templates, dest_dir)
    assert (dest_dir / "template1.j2").exists()
    assert (dest_dir / "template2.j2").exists()
    assert (dest_dir / "template1.j2").read_text() == "Template 1 content"
    assert (dest_dir / "template2.j2").read_text() == "Template 2 content"

def test_update_existing_templates(temp_dir, mock_package_templates):
    dest_dir = temp_dir / "dest"
    dest_dir.mkdir()
    (dest_dir / "template1.j2").write_text("Old content")
    create_templates_directory(mock_package_templates, dest_dir, force=True)
    assert (dest_dir / "template1.j2").read_text() == "Template 1 content"
    assert (dest_dir / "template2.j2").read_text() == "Template 2 content"

def test_permission_error(temp_dir, mock_package_templates):
    dest_dir = temp_dir / "dest"
    dest_dir.mkdir(mode=0o555)  # Read-only directory
    with pytest.raises(PermissionError):
        create_templates_directory(mock_package_templates, dest_dir)

def test_non_existent_source(temp_dir):
    with pytest.raises(FileNotFoundError):
        create_templates_directory(temp_dir / "non_existent", temp_dir / "dest")

@patch('builtins.input', return_value='y')
def test_user_confirmation(mock_input, temp_dir, mock_package_templates):
    dest_dir = temp_dir / "dest"
    dest_dir.mkdir()
    (dest_dir / "template1.j2").write_text("Old content")
    create_templates_directory(mock_package_templates, dest_dir)
    mock_input.assert_called_once()
    assert (dest_dir / "template1.j2").read_text() == "Template 1 content"

@patch('builtins.input', return_value='n')
def test_user_rejection(mock_input, temp_dir, mock_package_templates):
    dest_dir = temp_dir / "dest"
    dest_dir.mkdir()
    (dest_dir / "template1.j2").write_text("Old content")
    create_templates_directory(mock_package_templates, dest_dir)
    mock_input.assert_called_once()
    assert (dest_dir / "template1.j2").read_text() == "Old content"

@patch('code2prompt.utils.create_template_directory.logger')
def test_user_feedback(mock_logger, temp_dir, mock_package_templates):
    create_templates_directory(mock_package_templates, temp_dir / "dest")
    assert mock_logger.info.call_count >= 2  # At least two info logs

def test_dry_run(temp_dir, mock_package_templates):
    dest_dir = temp_dir / "dest"
    create_templates_directory(mock_package_templates, dest_dir, dry_run=True)
    assert not dest_dir.exists()

def test_force_overwrite(temp_dir, mock_package_templates):
    dest_dir = temp_dir / "dest"
    dest_dir.mkdir()
    (dest_dir / "template1.j2").write_text("Old content")
    create_templates_directory(mock_package_templates, dest_dir, force=True)
    assert (dest_dir / "template1.j2").read_text() == "Template 1 content"

def test_skip_existing(temp_dir, mock_package_templates):
    dest_dir = temp_dir / "dest"
    dest_dir.mkdir()
    (dest_dir / "template1.j2").write_text("Old content")
    create_templates_directory(mock_package_templates, dest_dir, skip_existing=True)
    assert (dest_dir / "template1.j2").read_text() == "Old content"
    assert (dest_dir / "template2.j2").read_text() == "Template 2 content"

def test_large_number_of_templates(temp_dir):
    package_templates = temp_dir / "package_templates"
    package_templates.mkdir()
    for i in range(100):
        (package_templates / f"template{i}.j2").write_text(f"Template {i} content")
    create_templates_directory(package_templates, temp_dir / "dest")
    assert len(list((temp_dir / "dest").glob("*.j2"))) == 100


def test_special_characters(temp_dir, mock_package_templates):
    (mock_package_templates / "special!@#$%^&*.j2").write_text("Special content")
    create_templates_directory(mock_package_templates, temp_dir / "dest")
    assert (temp_dir / "dest" / "special!@#$%^&*.j2").exists()
    assert (temp_dir / "dest" / "special!@#$%^&*.j2").read_text() == "Special content"

@patch('shutil.disk_usage')
def test_insufficient_disk_space(mock_disk_usage, temp_dir, mock_package_templates):
    mock_disk_usage.return_value = (100, 50, 10)  # total, used, free
    with pytest.raises(IOError, match="Insufficient disk space"):
        create_templates_directory(mock_package_templates, temp_dir / "dest")

