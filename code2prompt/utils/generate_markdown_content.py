def generate_markdown_content(files_data, no_codeblock):
    """
    Generates a Markdown content string from the provided files data.

    Parameters:
    - files_data (list of dict): A list of dictionaries containing file information and content.
    - no_codeblock (bool): Flag indicating whether to disable wrapping code inside markdown code blocks.

    Returns:
    - str: A Markdown-formatted string containing the table of contents and the file contents.
    """
    table_of_contents = [f"- {file['path']}\n" for file in files_data]
    
    content = []
    for file in files_data:
        file_info = (
            f"## File: {file['path']}\n\n"
            f"- Extension: {file['extension']}\n"
            f"- Language: {file['language']}\n"
            f"- Size: {file['size']} bytes\n"
            f"- Created: {file['created']}\n"
            f"- Modified: {file['modified']}\n\n"
        )
        
        if no_codeblock:
            file_code = f"### Code\n\n{file['content']}\n\n"
        else:
            file_code = f"### Code\n\n```{file['language']}\n{file['content']}\n```\n\n"
        
        content.append(file_info + file_code)
    
    return (
        "# Table of Contents\n"
        + "".join(table_of_contents)
        + "\n"
        + "".join(content)
    )
