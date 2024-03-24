""" A collection of functions to strip comments from code strings based on the programming language. """

import re


def strip_c_style_comments(code: str) -> str:
    """
    Strips C-style comments from the given code string.
    Supports single-line comments (//), multi-line comments (/* */), and string literals.

    :param code: The code string to strip comments from.
    :return: The code string with C-style comments removed.
    """
    pattern = re.compile(
        r'//.*?$|/\*.*?\*/|\'(?:\\.|[^\\\'])*\'|"(?:\\.|[^\\"])*"',
        re.DOTALL | re.MULTILINE,
    )
    return re.sub(
        pattern,
        lambda match: match.group(0) if match.group(0).startswith(("'", '"')) else "",
        code,
    )


def strip_html_style_comments(code: str) -> str:
    """
    Strips HTML-style comments from the given code string.
    Supports both single-line and multi-line comments (<!-- -->).

    :param code: The code string to strip comments from.
    :return: The code string with HTML-style comments removed.
    """
    pattern = re.compile(r"<!--.*?-->", re.DOTALL)
    return re.sub(pattern, "", code)


def strip_python_style_comments(code: str) -> str:
    """
    Strips Python-style comments from the given code string.
    Supports single-line comments (#), multi-line comments (''' ''' or \"\"\" \"\"\"), and string literals.

    :param code: The code string to strip comments from.
    :return: The code string with Python-style comments removed.
    """
    pattern = re.compile(
        r'(?s)#.*?$|\'\'\'.*?\'\'\'|""".*?"""|\'(?:\\.|[^\\\'])*\'|"(?:\\.|[^\\"])*"',
        re.MULTILINE,
    )
    return re.sub(
        pattern,
        lambda match: (
            "" if match.group(0).startswith(("#", "'''", '"""')) else match.group(0)
        ),
        code,
    )


def strip_shell_style_comments(code: str) -> str:
    """
    Strips shell-style comments from the given code string.
    Supports single-line comments (#) and multi-line comments (: ' ').

    :param code: The code string to strip comments from.
    :return: The code string with shell-style comments removed.
    """
    lines = code.split("\n")
    new_lines = []
    in_multiline_comment = False

    for line in lines:
        if line.strip().startswith("#!"):
            # Preserve shebang lines
            new_lines.append(line)
        elif in_multiline_comment:
            if line.strip().endswith("'"):
                in_multiline_comment = False
        elif line.strip().startswith(": '"):
            in_multiline_comment = True
        elif "#" in line:
            # Remove single-line comments
            line = line.split("#", 1)[0]
            if line.strip():
                new_lines.append(line)
        else:
            new_lines.append(line)

    return "\n".join(new_lines).strip()

def strip_sql_style_comments(code: str) -> str:
    """
    Strips SQL-style comments from the given code string.
    Supports single-line comments (--), multi-line comments (/* */), and string literals.

    :param code: The code string to strip comments from.
    :return: The code string with SQL-style comments removed.
    """
    pattern = re.compile(
        r'--.*?$|/\*.*?\*/|\'(?:\\.|[^\\\'])*\'|"(?:\\.|[^\\"])*"',
        re.DOTALL | re.MULTILINE,
    )
    return re.sub(
        pattern,
        lambda match: match.group(0) if match.group(0).startswith(("'", '"')) else "",
        code,
    )


def strip_matlab_style_comments(code: str) -> str:
    """
    Strips MATLAB-style comments from the given code string.
    Supports single-line comments (%) and string literals.

    :param code: The code string to strip comments from.
    :return: The code string with MATLAB-style comments removed.
    """
    pattern = re.compile(
        r'%.*?$|\'(?:\\.|[^\\\'])*\'|"(?:\\.|[^\\"])*"', re.DOTALL | re.MULTILINE
    )
    return re.sub(
        pattern,
        lambda match: match.group(0) if match.group(0).startswith(("'", '"')) else "",
        code,
    )


def strip_r_style_comments(code: str) -> str:
    """
    Strips R-style comments from the given code string.
    Supports single-line comments (#) and string literals.

    :param code: The code string to strip comments from.
    :return: The code string with R-style comments removed.
    """
    pattern = re.compile(
        r'#.*?$|\'(?:\\.|[^\\\'])*\'|"(?:\\.|[^\\"])*"', re.DOTALL | re.MULTILINE
    )
    return re.sub(
        pattern,
        lambda match: match.group(0) if match.group(0).startswith(("'", '"')) else "",
        code,
    )


def strip_comments(code: str, language: str) -> str:
    """
    Strips comments from the given code string based on the specified programming language.

    :param code: The code string to strip comments from.
    :param language: The programming language of the code.
    :return: The code string with comments removed.
    """
    if language in [
        "c",
        "cpp",
        "java",
        "javascript",
        "csharp",
        "php",
        "go",
        "rust",
        "kotlin",
        "swift",
        "scala",
        "dart",
    ]:
        return strip_c_style_comments(code)
    elif language in ["python", "ruby", "perl"]:
        return strip_python_style_comments(code)
    elif language in ["bash", "powershell", "shell"]:
        return strip_shell_style_comments(code)
    elif language in ["html", "xml"]:
        return strip_html_style_comments(code)
    elif language in ["sql", "plsql", "tsql"]:
        return strip_sql_style_comments(code)
    elif language in ["matlab", "octave"]:
        return strip_matlab_style_comments(code)
    elif language in ["r"]:
        return strip_r_style_comments(code)
    else:
        return code
