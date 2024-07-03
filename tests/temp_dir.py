import pytest


import os
from pathlib import Path


@pytest.fixture
def temp_dir(tmp_path):
    """Fixture to provide a temporary directory for testing."""
    original_cwd = Path.cwd()
    os.chdir(tmp_path)
    yield tmp_path
    os.chdir(original_cwd)