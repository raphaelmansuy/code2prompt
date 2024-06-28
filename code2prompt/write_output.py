import click


from pathlib import Path


def write_output(markdown_content, output_path):
    """
    Writes the generated markdown content to a file or prints it to the console.

    Parameters:
    - markdown_content (str): The markdown content to be written or printed.
    - output_path (str): The path to the file where the markdown content should be written. If None, the content is printed to the console.

    Returns:
    None
    """
    if output_path:
        with Path(output_path).open("w", encoding="utf-8") as md_file:
            md_file.write(markdown_content)
        click.echo(f"Markdown file '{output_path}' created successfully.")
    else:
        click.echo(markdown_content)
