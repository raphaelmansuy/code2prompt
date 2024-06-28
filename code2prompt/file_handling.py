from pathlib import Path
from fnmatch import fnmatch

def parse_gitignore(gitignore_path):
    if not gitignore_path.exists():
        return set()
    with gitignore_path.open("r", encoding="utf-8") as file:
        patterns = set(line.strip() for line in file if line.strip() and not line.startswith("#"))
    return patterns

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

def is_filtered(file_path, include_pattern="", exclude_pattern="", case_sensitive=False):
    def match_patterns(file_name, patterns):
        return any(fnmatch(file_name, pattern) for pattern in patterns)

    file_name = file_path.name
    if not case_sensitive:
        file_name = file_name.lower()
    include_patterns = [p.strip().lower() for p in (include_pattern or "").split(',') if p.strip()]
    exclude_patterns = [p.strip().lower() for p in (exclude_pattern or "").split(',') if p.strip()]

    if not include_patterns:
        include_match = True
    else:
        include_match = match_patterns(file_name, include_patterns)
    exclude_match = match_patterns(file_name, exclude_patterns)
    return include_match and not exclude_match

def is_binary(file_path):
    try:
        with open(file_path, "rb") as file:
            chunk = file.read(1024)
            return b"\x00" in chunk
    except IOError:
        print(f"Error: The file at {file_path} could not be opened.")
        return False
