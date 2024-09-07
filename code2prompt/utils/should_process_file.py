"""

This module contains the function to determine 
if a file should be processed based on several criteria.

"""

import logging
from pathlib import Path
from typing import List  # Add this import
from code2prompt.utils.is_binary import is_binary
from code2prompt.utils.is_filtered import is_filtered
from code2prompt.utils.is_ignored import is_ignored

logger = logging.getLogger(__name__)


def should_process_file(
    file_path: Path,
    gitignore_patterns: List[str],  # List is now defined
    root_path: Path,
    filter_patterns: str,  ## comma separated list of patterns
    exclude_patterns: str,  ## comma separated list of patterns
    case_sensitive: bool,
) -> bool:
    """
    Determine whether a file should be processed based on several criteria.
    """
    logger.debug(
        "Checking if should process file: %s", file_path
    )  # Use lazy % formatting

    if not file_path.is_file():
        logger.debug("Skipping %s: Not a file.", file_path)  # Use lazy % formatting
        return False

    if is_ignored(file_path, gitignore_patterns, root_path):
        logger.debug(
            "Skipping %s: File is ignored based on gitignore patterns.", file_path
        )
        return False

    if not is_filtered(
        file_path=file_path,
        include_pattern=filter_patterns,
        exclude_pattern=exclude_patterns,
        case_sensitive=case_sensitive,
    ):
        logger.debug(
            "Skipping %s: File does not meet filter criteria.", file_path
        )  # Use lazy % formatting
        return False

    if is_binary(file_path):
        logger.debug("Skipping %s: File is binary.", file_path)  # Use lazy % formatting
        return False

    logger.debug("Processing file: %s", file_path)  # Use lazy % formatting
    return True
