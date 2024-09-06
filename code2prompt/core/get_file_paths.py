"""
This module contains the function to get file paths based on the provided options.
"""

from pathlib import Path
from code2prompt.utils.get_gitignore_patterns import get_gitignore_patterns
from code2prompt.utils.should_process_file import should_process_file


def get_file_paths(options: dict) -> list:
    """
    Retrieves file paths based on the provided options.

    Args:
    options (dict): A dictionary containing options such as paths and gitignore patterns.

    Returns:
    list: A list of file paths that should be processed.
    """
    file_paths: list = []

    # Ensure 'path' is always a list for consistent processing
    paths = options["path"] if isinstance(options["path"], list) else [options["path"]]
    filter_patterns = options["filter"]
    exclude_patterns = options["exclude"]
    case_sensitive = options["case_sensitive"]

    for path in paths:
        path = Path(path)

        # Get gitignore patterns for the current path
        gitignore_patterns = get_gitignore_patterns(
            path.parent if path.is_file() else path, options["gitignore"]
        )

        if path.is_file():
            # Add single file path
            if should_process_file(
                path,
                gitignore_patterns,
                path.parent,
                filter_patterns,
                exclude_patterns,
                case_sensitive,
            ):
                file_paths.append(str(path))
        else:
            # Add directory file paths
            for file_path in path.rglob("*"):
                if should_process_file(
                    file_path,
                    gitignore_patterns,
                    path,
                    filter_patterns,
                    exclude_patterns,
                    case_sensitive,
                ):
                    file_paths.append(str(file_path))

    return file_paths
