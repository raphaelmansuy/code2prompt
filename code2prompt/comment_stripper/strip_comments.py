from .c_style import strip_c_style_comments
from .html_style import strip_html_style_comments
from .python_style import strip_python_style_comments
from .shell_style import strip_shell_style_comments
from .sql_style import strip_sql_style_comments
from .matlab_style import strip_matlab_style_comments
from .r_style import strip_r_style_comments

def strip_comments(code: str, language: str) -> str:
    if language in [
        "c", "cpp", "java", "javascript", "csharp", "php", "go", "rust", "kotlin", "swift", "scala", "dart",
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
