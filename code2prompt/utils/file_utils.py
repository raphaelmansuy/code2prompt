# code2prompt/utils/file_utils.py

from pathlib import Path
from typing import List, Dict, Any
import logging

from code2prompt.config import Configuration
from code2prompt.utils.is_binary import is_binary
from code2prompt.utils.is_filtered import is_filtered
from code2prompt.utils.is_ignored import is_ignored
from code2prompt.utils.get_gitignore_patterns import get_gitignore_patterns
from code2prompt.core.process_file import process_file

logger = logging.getLogger(__name__)

def process_files(config: Configuration) -> List[Dict[str, Any]]:
    """
    Process files based on the provided configuration.

    Args:
        config (Configuration): Configuration object containing processing options.

    Returns:
        List[Dict[str, Any]]: A list of dictionaries containing processed file data.
    """
    files_data = []
    for path in config.path:
        path = Path(path)
        gitignore_patterns = get_gitignore_patterns(
            path.parent if path.is_file() else path,
            config.gitignore
        )
        
        if path.is_file():
            file_data = process_single_file(path, gitignore_patterns, config)
            if file_data:
                files_data.append(file_data)
        else:
            files_data.extend(process_directory(path, gitignore_patterns, config))
    
    return files_data

def process_single_file(
    file_path: Path,
    gitignore_patterns: List[str],
    config: Configuration
) -> Dict[str, Any]:
    """
    Process a single file if it meets the criteria.

    Args:
        file_path (Path): Path to the file to process.
        gitignore_patterns (List[str]): List of gitignore patterns.
        config (Configuration): Configuration object containing processing options.

    Returns:
        Dict[str, Any]: Processed file data if the file should be processed, None otherwise.
    """
    if should_process_file(file_path, gitignore_patterns, file_path.parent, config):
        return process_file(
            file_path,
            config.suppress_comments,
            config.line_number,
            config.no_codeblock
        )
    return None

def process_directory(
    directory_path: Path,
    gitignore_patterns: List[str],
    config: Configuration
) -> List[Dict[str, Any]]:
    """
    Process all files in a directory that meet the criteria.

    Args:
        directory_path (Path): Path to the directory to process.
        gitignore_patterns (List[str]): List of gitignore patterns.
        config (Configuration): Configuration object containing processing options.

    Returns:
        List[Dict[str, Any]]: List of processed file data for files that meet the criteria.
    """
    files_data = []
    for file_path in directory_path.rglob("*"):
        if file_path.is_file():
            file_data = process_single_file(file_path, gitignore_patterns, config)
            if file_data:
                files_data.append(file_data)
    return files_data

def should_process_file(
    file_path: Path,
    gitignore_patterns: List[str],
    root_path: Path,
    config: Configuration
) -> bool:
    """
    Determine whether a file should be processed based on several criteria.

    Args:
        file_path (Path): Path to the file to check.
        gitignore_patterns (List[str]): List of gitignore patterns.
        root_path (Path): Root path for relative path calculations.
        config (Configuration): Configuration object containing processing options.

    Returns:
        bool: True if the file should be processed, False otherwise.
    """
    logger.debug(f"Checking if should process file: {file_path}")

    if not file_path.is_file():
        logger.debug(f"Skipping {file_path}: Not a file.")
        return False

    if is_ignored(file_path, gitignore_patterns, root_path):
        logger.debug(f"Skipping {file_path}: File is ignored based on gitignore patterns.")
        return False

    if not is_filtered(
        file_path,
        config.filter,
        config.exclude,
        config.case_sensitive
    ):
        logger.debug(f"Skipping {file_path}: File does not meet filter criteria.")
        return False

    if is_binary(file_path):
        logger.debug(f"Skipping {file_path}: File is binary.")
        return False

    logger.debug(f"Processing file: {file_path}")
    return True