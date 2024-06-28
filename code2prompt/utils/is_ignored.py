from fnmatch import fnmatch
from pathlib import Path


def is_ignored(file_path: Path, gitignore_patterns: list, base_path: Path) -> bool:
    relative_path = file_path.relative_to(base_path)
    for pattern in gitignore_patterns:
        pattern = pattern.rstrip("/")
        if pattern.startswith("/"):
            if fnmatch(str(relative_path), pattern[1:]):
                return True
            if fnmatch(str(relative_path.parent), pattern[1:]):
                return True
        else:
            for path in relative_path.parents:
                if fnmatch(str(path / relative_path.name), pattern):
                    return True
                if fnmatch(str(path), pattern):
                    return True
            if fnmatch(str(relative_path), pattern):
                return True
    return False