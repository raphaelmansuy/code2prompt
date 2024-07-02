from code2prompt.comment_stripper import strip_sql_style_comments
from tests.normalize_whitespace_1 import normalize_whitespace


from textwrap import dedent


def test_strip_sql_style_comments():
    """Test the strip_sql_style_comments function."""
    code = """
    SELECT *
    FROM table
    -- Single-line comment
    /* Multi-line
       comment */
    WHERE condition; -- Inline comment
    """
    expected = """
    SELECT *
    FROM table
    WHERE condition;
    """
    assert normalize_whitespace(strip_sql_style_comments(code)) == normalize_whitespace(dedent(expected))