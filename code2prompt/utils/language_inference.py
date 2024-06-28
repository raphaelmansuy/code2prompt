import os

def infer_language(filename: str) -> str:
    """
    Infers the programming language of a given file based on its extension.

    Parameters:
    - filename (str): The name of the file including its extension.

    Returns:
    - str: The inferred programming language as a lowercase string, e.g., "python".
           Returns "unknown" if the language cannot be determined.
    """
    _, extension = os.path.splitext(filename)
    extension = extension.lower()
    if extension in [".c", ".h"]:
        return "c"
    elif extension in [".cpp", ".hpp", ".cc", ".cxx"]:
        return "cpp"
    elif extension in [".java"]:
        return "java"
    elif extension in [".js", ".jsx"]:
        return "javascript"
    elif extension in [".cs"]:
        return "csharp"
    elif extension in [".php"]:
        return "php"
    elif extension in [".go"]:
        return "go"
    elif extension in [".rs"]:
        return "rust"
    elif extension in [".kt"]:
        return "kotlin"
    elif extension in [".swift"]:
        return "swift"
    elif extension in [".scala"]:
        return "scala"
    elif extension in [".dart"]:
        return "dart"
    elif extension in [".py"]:
        return "python"
    elif extension in [".rb"]:
        return "ruby"
    elif extension in [".pl", ".pm"]:
        return "perl"
    elif extension in [".sh"]:
        return "bash"
    elif extension in [".ps1"]:
        return "powershell"
    elif extension in [".html", ".htm"]:
        return "html"
    elif extension in [".xml"]:
        return "xml"
    elif extension in [".sql"]:
        return "sql"
    elif extension in [".m"]:
        return "matlab"
    elif extension in [".r"]:
        return "r"
    else:
        return "unknown"
