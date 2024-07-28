def add_line_numbers(code: str) -> str:
    """
    Adds line numbers to each line of the given code.

    Args:
        code (str): The code to add line numbers to.

    Returns:
        str: The code with line numbers added.
    """
    lines = code.splitlines()
    max_line_number = len(lines)
    line_number_width = len(str(max_line_number))
    numbered_lines = [f"{i+1:{line_number_width}} | {line}" for i, line in enumerate(lines)]
    return "\n".join(numbered_lines)