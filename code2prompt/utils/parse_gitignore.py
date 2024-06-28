def parse_gitignore(gitignore_path):
    if not gitignore_path.exists():
        return set()
    with gitignore_path.open("r", encoding="utf-8") as file:
        patterns = set(line.strip() for line in file if line.strip() and not line.startswith("#"))
    return patterns