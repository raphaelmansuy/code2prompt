from code2prompt.utils.parse_gitignore import parse_gitignore
from pathlib import Path

def get_gitignore_patterns(path, gitignore):
    """
    Retrieve gitignore patterns from a specified path or a default .gitignore file.

    This function reads the .gitignore file located at the specified path or uses
    the default .gitignore file in the project root if no specific path is provided.
    It then parses the file to extract ignore patterns and adds a default pattern
    to ignore the .git directory itself.

    Args:
    path (Path): The root path of the project where the default .gitignore file is located.
    gitignore (Optional[str]): An optional path to a specific .gitignore file to use instead of the default.

    Returns:
    Set[str]: A set of gitignore patterns extracted from the .gitignore file.
    """
    if gitignore:
        gitignore_path = Path(gitignore)
    else:
        gitignore_path = Path(path) / ".gitignore"

    patterns = parse_gitignore(gitignore_path)
    patterns.add(".git")
    return patterns