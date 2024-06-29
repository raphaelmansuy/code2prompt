import click
from pathlib import Path
import pyperclip

def write_output(content, output_path):
    """
    Writes the generated content to a file or prints it to the console,
    and copies the content to the clipboard.

    Parameters:
    - content (str): The content to be written, printed, and copied.
    - output_path (str): The path to the file where the content should be written.
                         If None, the content is printed to the console.

    Returns:
    None
    """
    if output_path:
        try:
            with Path(output_path).open("w", encoding="utf-8") as output_file:
                output_file.write(content)
            click.echo(f"Output file '{output_path}' created successfully.")
        except IOError as e:
            click.echo(f"Error writing to output file: {e}", err=True)
    else:
        click.echo(content)

    # Copy content to clipboard
    try:
        pyperclip.copy(content)
    except Exception as e:
        click.echo(f"Error copying to clipboard: {e}", err=True)