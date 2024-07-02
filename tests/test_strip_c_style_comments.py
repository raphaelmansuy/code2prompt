from code2prompt.comment_stripper import strip_c_style_comments
from tests.normalize_whitespace_1 import normalize_whitespace


from textwrap import dedent


def test_strip_c_style_comments():
    """Test the strip_c_style_comments function."""
    code = """
    int main() {
        // Single-line comment
        /* Multi-line
           comment */
        printf("Hello, World!"); // Inline comment
    }
    """
    expected = """
    int main() {
        printf("Hello, World!");
    }
    """
    assert normalize_whitespace(strip_c_style_comments(code)) == normalize_whitespace(dedent(expected))