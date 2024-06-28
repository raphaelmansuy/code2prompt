import re

def strip_html_style_comments(code: str) -> str:
    pattern = re.compile(r"<!--.*?-->", re.DOTALL)
    return re.sub(pattern, "", code)
