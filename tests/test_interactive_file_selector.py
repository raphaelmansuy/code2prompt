import pytest
from unittest.mock import patch, MagicMock
from code2prompt.commands.interactive_selector import InteractiveFileSelector
from pathlib import Path


@pytest.fixture
def interactive_file_selector():
    with patch('os.get_terminal_size') as mock_get_terminal_size:
        mock_get_terminal_size.return_value.lines = 20  # Mock terminal height
        selector = InteractiveFileSelector([str(Path.home())])  # Use home directory for testing
        yield selector


def test_check_paths_valid(interactive_file_selector):
    interactive_file_selector.check_paths()  # Should not raise an error


def test_check_paths_invalid_empty():
    selector = InteractiveFileSelector([])
    with pytest.raises(ValueError):
        selector.check_paths()


def test_check_paths_invalid_none():
    selector = InteractiveFileSelector([None])
    with pytest.raises(ValueError):
        selector.check_paths()


@patch('pathlib.Path.rglob')
def test_get_directory_tree(mock_rglob, interactive_file_selector):
    mock_rglob.return_value = [Path('file1.txt'), Path('file2.txt')]
    tree = interactive_file_selector.get_directory_tree()
    assert 'file1.txt' in tree
    assert 'file2.txt' in tree


def test_format_tree(interactive_file_selector):
    tree = {'file1.txt': {}, 'file2.txt': {}}
    formatted = interactive_file_selector.format_tree(tree)
    assert formatted == ['└── file1.txt', '└── file2.txt']


def test_toggle_file_selection(interactive_file_selector):
    interactive_file_selector.toggle_file_selection('file1.txt')
    assert str(Path.home() / 'file1.txt') in interactive_file_selector.selected_files
    interactive_file_selector.toggle_file_selection('file1.txt')
    assert str(Path.home() / 'file1.txt') not in interactive_file_selector.selected_files


def test_get_current_item(interactive_file_selector):
    interactive_file_selector.formatted_tree = ['└── file1.txt', '└── file2.txt']
    interactive_file_selector.cursor_position = 0
    current_item = interactive_file_selector.get_current_item()
    assert current_item == 'file1.txt'


@patch('code2prompt.commands.interactive_selector.Application.run')
def test_run(mock_run, interactive_file_selector):
    interactive_file_selector.run()  # Should not raise an error
    mock_run.assert_called_once()


def test_get_visible_lines(interactive_file_selector):
    visible_lines = interactive_file_selector.get_visible_lines()
    assert visible_lines == 17  # 20 - 3 (for instructions and padding)