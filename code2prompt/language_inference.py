"""
This module contains the function to infer the programming language based on the file extension.
"""

import os


def infer_language(filename: str) -> str:
    """
    Infers the programming language based on the file extension.

    :param filename: The name of the file.
    :return: The inferred programming language.
    """
    _, extension = os.path.splitext(filename)
    extension = extension.lower()

    language_map = {
        ".c": "c",
        ".h": "c",
        ".cpp": "cpp",
        ".hpp": "cpp",
        ".cc": "cpp",
        ".cxx": "cpp",
        ".java": "java",
        ".js": "javascript",
        ".jsx": "javascript",
        ".cs": "csharp",
        ".php": "php",
        ".go": "go",
        ".rs": "rust",
        ".kt": "kotlin",
        ".swift": "swift",
        ".scala": "scala",
        ".dart": "dart",
        ".py": "python",
        ".rb": "ruby",
        ".pl": "perl",
        ".pm": "perl",
        ".sh": "bash",
        ".ps1": "powershell",
        ".html": "html",
        ".htm": "html",
        ".xml": "xml",
        ".sql": "sql",
        ".m": "matlab",
        ".r": "r"
    }

    return language_map.get(extension, "unknown")