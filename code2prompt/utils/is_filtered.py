from fnmatch import fnmatch


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