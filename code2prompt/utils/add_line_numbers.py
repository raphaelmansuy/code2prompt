def add_line_numbers(code: str) -> str:
    lines = code.splitlines()
    max_line_number = len(lines)
    line_number_width = len(str(max_line_number))
    numbered_lines = [f"{i+1:{line_number_width}} | {line}" for i, line in enumerate(lines)]
    return "\n".join(numbered_lines)