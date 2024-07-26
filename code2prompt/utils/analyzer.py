from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Tuple

def analyze_codebase(path: str) -> Tuple[Dict[str, int], Dict[str, List[str]]]:
    """
    Analyze the codebase and return file extension information.
    
    Args:
        path (str): The path to the codebase directory.
    
    Returns:
        Tuple[Dict[str, int], Dict[str, List[str]]]: A tuple containing:
            - A dictionary of file extensions and their counts.
            - A dictionary of file extensions and the directories containing them.
    """
    extension_counts = defaultdict(int)
    extension_dirs = defaultdict(set)
    
    file_count = 0
    for file_path in Path(path).rglob('*'):
        if file_path.is_file():
            file_count += 1
            ext = file_path.suffix.lower()
            if ext:
                extension_counts[ext] += 1
                extension_dirs[ext].add(str(file_path.parent))
    
    if file_count == 0:
        return {"No files found": 0}, {}
    
    return dict(extension_counts), {k: list(v) for k, v in extension_dirs.items()}
    

def format_flat_output(extension_counts: Dict[str, int]) -> str:
    """
    Format the analysis results in a flat structure.
    
    Args:
        extension_counts (Dict[str, int]): A dictionary of file extensions and their counts.
    
    Returns:
        str: Formatted output string.
    """
    output = []
    for ext, count in sorted(extension_counts.items()):
        output.append(f"{ext}: {count} file{'s' if count > 1 else ''}")
    return "\n".join(output)

def format_tree_output(extension_dirs: Dict[str, List[str]]) -> str:
    """
    Format the analysis results in a tree-like structure.
    
    Args:
        extension_dirs (Dict[str, List[str]]): A dictionary of file extensions and their directories.
    
    Returns:
        str: Formatted output string.
    """
    def format_tree(node, prefix=""):
        output = []
        for i, (key, value) in enumerate(node.items()):
            is_last = i == len(node) - 1
            output.append(f"{prefix}{'└── ' if is_last else '├── '}{key}")
            if isinstance(value, dict):
                extension = "    " if is_last else "│   "
                output.extend(format_tree(value, prefix + extension))
        return output

    tree = {}
    for ext, dirs in extension_dirs.items():
        for dir_path in dirs:
            current = tree
            for part in Path(dir_path).parts:
                current = current.setdefault(part, {})
            current[ext] = {}

    return "\n".join(format_tree(tree))

def get_extension_list(extension_counts: Dict[str, int]) -> str:
    """
    Generate a comma-separated list of file extensions.
    
    Args:
        extension_counts (Dict[str, int]): A dictionary of file extensions and their counts.
    
    Returns:
        str: Comma-separated list of file extensions.
    """
    return ",".join(sorted(extension_counts.keys()))