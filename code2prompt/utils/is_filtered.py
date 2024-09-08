"""
This module contains utility functions for filtering files based on include and exclude patterns.
"""

from pathlib import Path
from fnmatch import fnmatch


def is_filtered(
    file_path: Path,
    include_pattern: str = "",
    exclude_pattern: str = "",
    case_sensitive: bool = False,
) -> bool:
    """
    Determine if a file should be filtered based on include and exclude patterns.

    Parameters:
    - file_path (Path): Path to the file to check
    - include_pattern (str): Comma-separated list of patterns to include files
    - exclude_pattern (str): Comma-separated list of patterns to exclude files
    - case_sensitive (bool): Whether to perform case-sensitive pattern matching

    Returns:
    - bool: True if the file should be included, False if it should be filtered out
    """

    def match_pattern(path: str, pattern: str) -> bool:
        if "**" in pattern:
            parts = pattern.split("**")
            return any(fnmatch(path, f"*{p}*") for p in parts if p)
        return fnmatch(path, pattern)

    def match_patterns(path: str, patterns: list) -> bool:
        return any(match_pattern(path, pattern) for pattern in patterns)

    # Convert file_path to string
    file_path_str = str(file_path)

    # Handle case sensitivity
    if not case_sensitive:
        file_path_str = file_path_str.lower()

    # Prepare patterns
    def prepare_patterns(pattern):
        if isinstance(pattern, str):
            return [p.strip().lower() for p in pattern.split(",") if p.strip()]
        elif isinstance(pattern, (list, tuple)):
            return [str(p).strip().lower() for p in pattern if str(p).strip()]
        else:
            return []

    include_patterns = prepare_patterns(include_pattern)
    exclude_patterns = prepare_patterns(exclude_pattern)

    # If no patterns are specified, include the file
    if not include_patterns and not exclude_patterns:
        return True

    # Check exclude patterns first (they take precedence)
    if match_patterns(file_path_str, exclude_patterns):
        return False  # Exclude dotfiles and other specified patterns

    # If include patterns are specified, the file must match at least one
    if include_patterns:
        return match_patterns(file_path_str, include_patterns)

    # If we reach here, there were no include patterns and the file wasn't excluded
    return True
