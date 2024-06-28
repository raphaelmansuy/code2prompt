def strip_shell_style_comments(code: str) -> str:
    lines = code.split("\n")
    new_lines = []
    in_multiline_comment = False
    for line in lines:
        if line.strip().startswith("#!"):  # Preserve shebang lines
            new_lines.append(line)
        elif in_multiline_comment:
            if line.strip().endswith("'"):
                in_multiline_comment = False
        elif line.strip().startswith(": '"):
            in_multiline_comment = True
        elif "#" in line:  # Remove single-line comments
            line = line.split("#", 1)[0]
            if line.strip():
                new_lines.append(line)
        else:
            new_lines.append(line)
    return "\n".join(new_lines).strip()
