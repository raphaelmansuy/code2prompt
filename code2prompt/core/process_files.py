from pathlib import Path
from code2prompt.utils.get_gitignore_patterns import get_gitignore_patterns
from code2prompt.core.process_file import process_file
from code2prompt.utils.should_process_file import should_process_file

def process_files(options):
    """
    Processes files or directories based on the provided paths.

    Args:
    options (dict): A dictionary containing options such as paths, gitignore patterns,
                    and flags for processing files.

    Returns:
    list: A list of dictionaries containing processed file data.
    """
    files_data = []

    # Use get_file_paths to retrieve all file paths to process
    file_paths = get_file_paths(options)

    for path in file_paths:
        path = Path(path)
        result = process_file(
            path,
            options['suppress_comments'],
            options['line_number'],
            options['no_codeblock']
        )
        if result:
            files_data.append(result)

    return files_data

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
    paths = options['path'] if isinstance(options['path'], list) else [options['path']]

    for path in paths:
        path = Path(path)
        
        # Get gitignore patterns for the current path
        gitignore_patterns = get_gitignore_patterns(
            path.parent if path.is_file() else path,
            options['gitignore']
        )

        if path.is_file():
            # Add single file path
            if should_process_file(path, gitignore_patterns, path.parent, options):
                file_paths.append(str(path))
        else:
            # Add directory file paths
            for file_path in path.rglob("*"):
                if should_process_file(file_path, gitignore_patterns, path, options):
                    file_paths.append(str(file_path))

    return file_paths
