"""
This module contains functions for processing files and directories.
"""

from pathlib import Path
from code2prompt.core.process_file import process_file


def process_files(
    file_paths: list[Path],
    suppress_comments: bool,
    line_number: bool,
    no_codeblock: bool,
):
    """
    Processes files or directories based on the provided paths.

    Args:
    options (dict): A dictionary containing options such as paths, gitignore patterns,
                    and flags for processing files.

    Returns:
    list: A list of dictionaries containing processed file data.
    """
    files_data = []
    
    # Test file paths if List[Path] type
    if not (isinstance(file_paths, list) and all(isinstance(path, Path) for path in file_paths)): 
        raise ValueError("file_paths must be a list of Path objects")

    # Use get_file_paths to retrieve all file paths to process
    for path in file_paths:
        path = Path(path)
        result = process_file(
            file_path=path,
            suppress_comments=suppress_comments,
            line_number=line_number,
            no_codeblock=no_codeblock,
        )
        if result:
            files_data.append(result)

    return files_data
