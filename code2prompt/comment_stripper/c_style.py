import re

def strip_c_style_comments(code: str) -> str:
    pattern = re.compile(
        r'//.*?$|/\*.*?\*/|\'(?:\\.|[^\\\'])*\'|"(?:\\.|[^\\"])*"',
        re.DOTALL | re.MULTILINE,
    )
    return re.sub(
        pattern,
        lambda match: match.group(0) if match.group(0).startswith(("'", '"')) else "",
        code,
    )
