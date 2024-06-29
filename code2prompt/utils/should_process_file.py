from code2prompt.utils.is_binary import is_binary
from code2prompt.utils.is_filtered import is_filtered
from code2prompt.utils.is_ignored import is_ignored

def should_process_file(file_path, gitignore_patterns, root_path, options):
    """
    Determine whether a file should be processed based on several criteria.

    Args:
    file_path (Path): The path to the file being considered.
    gitignore_patterns (set): A set of patterns to ignore files.
    root_path (Path): The root path of the project for relative comparisons.
    options (dict): A dictionary of options including filter, exclude, and case sensitivity settings.

    Returns:
    bool: True if the file should be processed, False otherwise.
    """
    return (
        file_path.is_file()
        and not is_ignored(file_path, gitignore_patterns, root_path)
        and is_filtered(file_path, options['filter'], options['exclude'], options['case_sensitive'])
        and not is_binary(file_path)
    )