from code2prompt.comment_stripper import strip_r_style_comments
from tests.normalize_whitespace_1 import normalize_whitespace


from textwrap import dedent


def test_strip_r_style_comments():
    """Test the strip_r_style_comments function."""
    code = """
    # Single-line comment
    foo <- function(x) {
        # Multi-line
        # comment
        return(x + 1) # Inline comment
    }
    """
    expected = """
    foo <- function(x) {
        return(x + 1)
    }
    """
    assert normalize_whitespace(strip_r_style_comments(code)) == normalize_whitespace(dedent(expected))