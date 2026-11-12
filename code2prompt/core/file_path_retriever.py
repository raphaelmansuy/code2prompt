"""
This module contains the function to get file paths based on the provided options.
"""

import logging
import os
from pathlib import Path
from code2prompt.utils.get_gitignore_patterns import get_gitignore_patterns
from code2prompt.utils.is_filtered import is_filtered
from code2prompt.utils.should_process_file import should_process_file

logger = logging.getLogger(__name__)


def is_excluded_directory(
    dir_path: Path,
    exclude_patterns: list[str],
    case_sensitive: bool,
) -> bool:
    """
    True if every file under dir_path would be excluded anyway.

    Probed with a synthetic child path through the same is_filtered()
    matcher used for files, so pruning never changes which files are
    returned — it only skips descending into a directory whose contents
    are all excluded (e.g. `node_modules/**` prunes `node_modules`,
    while `*.log` prunes nothing because a directory can hold other
    files). A bare `node_modules` pattern (no `/**`) does not prune,
    matching today's file-level behavior where it excludes no contents.
    """
    if not exclude_patterns:
        return False
    probe = dir_path / "__code2prompt_probe__"
    return not is_filtered(
        file_path=probe,
        include_pattern="",
        exclude_pattern=exclude_patterns,
        case_sensitive=case_sensitive,
    )


def _iterate_directories(
    root: Path,
    exclude_patterns: list[str],
    case_sensitive: bool,
):
    """
    Mirror _RecursiveWildcardSelector._iterate_directories (what
    Path.rglob("*") uses): the root, then — for each directory os.walk
    visits, in order — its immediate subdirectories. Excluded
    directories are dropped from os.walk's dirnames, so neither they nor
    anything under them is ever yielded as a starting point.
    """
    yield root
    for dirpath, dirnames, _ in os.walk(root, topdown=True):
        kept = []
        for name in dirnames:
            dir_entry = Path(dirpath) / name
            if is_excluded_directory(dir_entry, exclude_patterns, case_sensitive):
                logger.debug("Skipping excluded directory: %s", dir_entry)
            else:
                kept.append(name)
        dirnames[:] = kept
        for name in dirnames:
            yield Path(dirpath) / name


def _iter_tree(
    root: Path,
    exclude_patterns: list[str],
    case_sensitive: bool,
):
    """
    Yield every entry under root, in the same order as Path.rglob("*"):
    for each directory in _iterate_directories order, that directory's
    entries. Symlinked directories are yielded as entries but not
    descended into beyond their immediate entries, like rglob.
    """
    for starting_point in _iterate_directories(root, exclude_patterns, case_sensitive):
        try:
            with os.scandir(starting_point) as it:
                entries = list(it)
        except OSError:
            continue
        for entry in entries:
            yield Path(entry.path)


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

            # Add files and directories within the top-level directory,
            # pruning directories whose contents are all excluded.
            for file_path in _iter_tree(path, exclude_patterns, case_sensitive):
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
