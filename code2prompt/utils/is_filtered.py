from pathlib import Path
from fnmatch import fnmatch

def is_filtered(file_path, include_pattern="", exclude_pattern="", case_sensitive=False):
    """
    Determine if a file should be filtered based on include and exclude patterns.
    
    Args:
    - file_path (Path): Path to the file to check
    - include_pattern (str): Comma-separated list of patterns to include files
    - exclude_pattern (str): Comma-separated list of patterns to exclude files
    - case_sensitive (bool): Whether to perform case-sensitive pattern matching
    
    Returns:
    - bool: True if the file should be included, False if it should be filtered out
    """
    def match_pattern(path, pattern):
        if "**" in pattern:
            parts = pattern.split("**")
            return path.match(pattern) or any(path.match(f"*{p}") for p in parts if p)
        return fnmatch(str(path), pattern) or fnmatch(path.name, pattern)

    def match_patterns(path, patterns):
        return any(match_pattern(path, pattern) for pattern in patterns)

    if not case_sensitive:
        file_path = Path(str(file_path).lower())
        include_pattern = include_pattern.lower()
        exclude_pattern = exclude_pattern.lower()

    include_patterns = [p.strip() for p in include_pattern.split(',') if p.strip()]
    exclude_patterns = [p.strip() for p in exclude_pattern.split(',') if p.strip()]

    # If no patterns are specified, include the file
    if not include_patterns and not exclude_patterns:
        return True

    # Check exclude patterns first (they take precedence)
    if match_patterns(file_path, exclude_patterns):
        return False

    # If include patterns are specified, the file must match at least one
    if include_patterns:
        return match_patterns(file_path, include_patterns)

    # If we reach here, there were no include patterns and the file wasn't excluded
    return True