from code2prompt.comment_stripper import strip_shell_style_comments
from tests.normalize_whitespace_1 import normalize_whitespace


from textwrap import dedent


def test_strip_shell_style_comments():
    """Test the strip_shell_style_comments function."""
    code = """
    #!/bin/bash
    # Single-line comment
    : '
    Multi-line
    comment
    '
    echo "Hello, World!" # Inline comment
    """
    expected = """
    #!/bin/bash
    echo "Hello, World!"
    """
    assert normalize_whitespace(strip_shell_style_comments(code)) == normalize_whitespace(dedent(expected))