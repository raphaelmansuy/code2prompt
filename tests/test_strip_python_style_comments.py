from code2prompt.comment_stripper import strip_python_style_comments
from tests.normalize_whitespace_1 import normalize_whitespace


from textwrap import dedent


def test_strip_python_style_comments():
    """Test the strip_python_style_comments function."""
    code = """
    def main():
        # Single-line comment
        '''
        Multi-line
        comment
        '''
        print("Hello, World!") # Inline comment
    """
    expected = """
    def main():
        print("Hello, World!")
    """
    assert normalize_whitespace(strip_python_style_comments(code)) == normalize_whitespace(dedent(expected))