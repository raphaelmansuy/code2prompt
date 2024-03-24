"""Tests for the comment_stripper module."""
import re
from textwrap import dedent
from code2prompt.comment_stripper import (
    strip_c_style_comments,
    strip_python_style_comments,
    strip_shell_style_comments,
    strip_html_style_comments,
    strip_matlab_style_comments,
    strip_sql_style_comments,
    strip_r_style_comments,
)


def normalize_whitespace(text):
    """ Normalize the whitespace in a string."""
    return re.sub(r'\s+', ' ', text.strip())


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