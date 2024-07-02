def test_add_line_numbers():
    # Sample content to test
    content = """First line
Second line
Third line"""

    # Expected output with line numbers added
    expected_output = """1: First line
2: Second line
3: Third line"""

    # Function to add line numbers
    def add_line_numbers(content):
        lines = content.split('\n')
        numbered_lines = [f"{i + 1}: {line}" for i, line in enumerate(lines)]
        return '\n'.join(numbered_lines)

    # Actual output from the function
    actual_output = add_line_numbers(content)

    # Assert that the actual output matches the expected output
    assert actual_output == expected_output, "Line numbers were not added correctly."