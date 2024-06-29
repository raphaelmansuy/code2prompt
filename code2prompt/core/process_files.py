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
            # Process single file
            if should_process_file(path, gitignore_patterns, path.parent, options):
                result = process_file(
                    path,
                    options['suppress_comments'],
                    options['line_number'],
                    options['no_codeblock']
                )
                if result:
                    files_data.append(result)
        else:
            # Process directory
            for file_path in path.rglob("*"):
                if should_process_file(file_path, gitignore_patterns, path, options):
                    result = process_file(
                        file_path,
                        options['suppress_comments'],
                        options['line_number'],
                        options['no_codeblock']
                    )
                    if result:
                        files_data.append(result)

    return files_data