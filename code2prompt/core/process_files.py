from pathlib import Path
from code2prompt.core.get_file_paths import get_file_paths
from code2prompt.core.process_file import process_file


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
            options["suppress_comments"],
            options["line_number"],
            options["no_codeblock"],
        )
        if result:
            files_data.append(result)

    return files_data


