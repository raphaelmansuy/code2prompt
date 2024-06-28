import re

def strip_python_style_comments(code: str) -> str:
    pattern = re.compile(
        r'(?s)#.*?$|\'\'\'.*?\'\'\'|""".*?"""|\'(?:\\.|[^\\\'])*\'|"(?:\\.|[^\\"])*"',
        re.MULTILINE,
    )
    return re.sub(
        pattern,
        lambda match: ("" if match.group(0).startswith(("#", "'''", '"""')) else match.group(0)),
        code,
    )
