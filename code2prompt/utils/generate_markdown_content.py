def generate_markdown_content(files_data, no_codeblock):
    """
    Generates a Markdown content string from the provided files data.

    This function takes a list of tuples where each tuple contains the file content and the file path.
    It constructs a table of contents and combines it with the file contents to produce a Markdown-formatted string.

    Parameters:
    - files_data (list of tuple): A list of tuples where each tuple contains the file content and the file path.
    - no_codeblock (bool): Flag indicating whether to disable wrapping code inside markdown code blocks.

    Returns:
    - str: A Markdown-formatted string containing the table of contents and the file contents.
    """
    table_of_contents = [f"- {file_path}\n" for _, file_path in files_data]
    content = [file_content for file_content, _ in files_data]

    if no_codeblock:
        # Remove any remaining code block markers
        content = [c.replace("```", "") for c in content]

    return (
        "# Table of Contents\n"
        + "".join(table_of_contents)
        + "\n"
        + "".join(content)
    )
