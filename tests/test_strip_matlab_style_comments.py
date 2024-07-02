from code2prompt.comment_stripper import strip_matlab_style_comments
from tests.normalize_whitespace_1 import normalize_whitespace


from textwrap import dedent


def test_strip_matlab_style_comments():
    """Test the strip_matlab_style_comments function."""
    code = """
    % Single-line comment
    function y = foo(x)
        % Multi-line
        % comment
        y = x + 1; % Inline comment
    end
    """
    expected = """
    function y = foo(x)
        y = x + 1;
    end
    """
    assert normalize_whitespace(strip_matlab_style_comments(code)) == normalize_whitespace(dedent(expected))