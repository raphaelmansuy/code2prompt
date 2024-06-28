from pathlib import Path
from code2prompt.get_gitignore_patterns import get_gitignore_patterns
from code2prompt.process_file import process_file
from code2prompt.should_process_file import should_process_file

def process_files(options):
    """
    Processes files or a single file based on the provided path.
    
    Args:
    options (dict): A dictionary containing options such as path, gitignore patterns, and flags for processing files.
    
    Returns:
    list: A list of dictionaries containing processed file data.
    """
    path = Path(options['path'])
    gitignore_patterns = get_gitignore_patterns(path.parent if path.is_file() else path, options['gitignore'])
    files_data = []

    if path.is_file():
        # Process single file
        if should_process_file(path, gitignore_patterns, path.parent, options):
            result = process_file(path, options['suppress_comments'], options['line_number'], options['no_codeblock'])
            if result:
                files_data.append(result)
    else:
        # Process directory
        for file_path in path.rglob("*"):
            if should_process_file(file_path, gitignore_patterns, path, options):
                result = process_file(file_path, options['suppress_comments'], options['line_number'], options['no_codeblock'])
                if result:
                    files_data.append(result)

    return files_data