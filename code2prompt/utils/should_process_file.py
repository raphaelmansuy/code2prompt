import logging
from code2prompt.utils.is_binary import is_binary
from code2prompt.utils.is_filtered import is_filtered
from code2prompt.utils.is_ignored import is_ignored

logger = logging.getLogger(__name__)


def should_process_file(file_path, gitignore_patterns, root_path, options):
    """
    Determine whether a file should be processed based on several criteria.
    """
    logger.debug(f"Checking if should process file: {file_path}")

    if not file_path.is_file():
        logger.debug(f"Skipping {file_path}: Not a file.")
        return False

    if is_ignored(file_path, gitignore_patterns, root_path):
        logger.debug(
            f"Skipping {file_path}: File is ignored based on gitignore patterns."
        )
        return False

    if not is_filtered(
        file_path,
        options.get("filter", ""),
        options.get("exclude", ""),
        options.get("case_sensitive", False),
    ):
        logger.debug(f"Skipping {file_path}: File does not meet filter criteria.")
        return False

    if is_binary(file_path):
        logger.debug(f"Skipping {file_path}: File is binary.")
        return False

    logger.debug(f"Processing file: {file_path}")
    return True
