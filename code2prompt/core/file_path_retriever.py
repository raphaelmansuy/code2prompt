"""
This module contains the function to get file paths based on the provided options.
"""

from pathlib import Path
from code2prompt.utils.get_gitignore_patterns import get_gitignore_patterns
from code2prompt.utils.should_process_file import should_process_file


def retrieve_file_paths(
    file_paths: list[Path],
    filter_patterns: list[str],
    exclude_patterns: list[str],
    case_sensitive: bool,
    gitignore: list[str],
) -> list[Path]:
    """
    Retrieves file paths based on the provided options.

    Args:
    file_paths (list[Path]): A list of paths to retrieve.
    filter_patterns (list[str]): Patterns to include.
    exclude_patterns (list[str]): Patterns to exclude.
    case_sensitive (bool): Whether the filtering should be case sensitive.
    gitignore (list[str]): Gitignore patterns to consider.

    Returns:
    list[Path]: A list of file paths that should be processed.
    """
    if not file_paths:
        raise ValueError("file_paths list cannot be empty.")

    retrieved_paths: list[Path] = []

    for path in file_paths:
        try:
            path = Path(path)

            # Get gitignore patterns for the current path
            gitignore_patterns = get_gitignore_patterns(
                path.parent if path.is_file() else path, gitignore
            )

            # Add the top-level directory if it should be processed
            if path.is_dir() and should_process_file(
                path,
                gitignore_patterns,
                path.parent,
                filter_patterns,
                exclude_patterns,
                case_sensitive,
            ):
                retrieved_paths.append(path)

            # Add files and directories within the top-level directory
            for file_path in path.rglob("*"):
                if should_process_file(
                    file_path,
                    gitignore_patterns,
                    path,
                    filter_patterns,
                    exclude_patterns,
                    case_sensitive,
                ):
                    retrieved_paths.append(file_path)

        except (FileNotFoundError, PermissionError) as e:
            print(f"Error processing path {path}: {e}")

    return retrieved_paths