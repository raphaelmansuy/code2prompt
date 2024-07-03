from code2prompt.comment_stripper import strip_html_style_comments
from tests.normalize_whitespace_1 import normalize_whitespace


from textwrap import dedent


def test_strip_html_style_comments():
    """Test the strip_html_style_comments function."""
    code = """
    <!DOCTYPE html>
    <html>
    <!-- Single-line comment -->
    <!--
    Multi-line
    comment
    -->
    <body>Hello, World!</body> <!-- Inline comment -->
    </html>
    """
    expected = """
    <!DOCTYPE html>
    <html>
    <body>Hello, World!</body>
    </html>
    """
    assert normalize_whitespace(strip_html_style_comments(code)) == normalize_whitespace(dedent(expected))