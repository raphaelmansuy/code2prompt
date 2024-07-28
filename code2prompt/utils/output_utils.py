# code2prompt/utils/output_utils.py

from pathlib import Path
import logging
from typing import Dict, List, Optional

from rich import print as rprint
from rich.panel import Panel
from rich.syntax import Syntax

from code2prompt.config import Configuration


def generate_content(files_data: List[Dict], config: Configuration) -> str:
    """
    Generate content based on the provided files data and configuration.

    Args:
        files_data (List[Dict]): A list of dictionaries containing processed file data.
        config (Configuration): Configuration object containing options.

    Returns:
        str: The generated content as a string.
    """
    if config.template:
        return _process_template(files_data, config)
    return _generate_markdown_content(files_data, config.no_codeblock)


def _process_template(files_data: List[Dict], config: Configuration) -> str:
    """
    Process a Jinja2 template with the given files data and user inputs.

    Args:
        files_data (List[Dict]): A list of dictionaries containing processed file data.
        config (Configuration): Configuration object containing options.

    Returns:
        str: The processed template content.
    """
    from code2prompt.core.template_processor import (
        get_user_inputs,
        load_template,
        process_template,
    )

    template_content = load_template(config.template)
    user_inputs = get_user_inputs(template_content)
    return process_template(template_content, files_data, user_inputs, config.template)


def _generate_markdown_content(files_data: List[Dict], no_codeblock: bool) -> str:
    """
    Generate markdown content from the provided files data.

    Args:
        files_data (List[Dict]): A list of dictionaries containing file information and content.
        no_codeblock (bool): Flag indicating whether to disable wrapping code inside markdown code blocks.

    Returns:
        str: A Markdown-formatted string containing the table of contents and the file contents.
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

    return "# Table of Contents\n" + "".join(table_of_contents) + "\n" + "".join(content)


def write_output(content: str, output_path: Optional[Path], logger: logging.Logger):
    """
    Write the generated content to a file or print it to the console.

    Args:
        content (str): The content to be written or printed.
        output_path (Optional[Path]): The path to the file where the content should be written.
                                      If None, the content is printed to the console.
        logger (logging.Logger): Logger instance for logging messages.
    """
    if output_path:
        try:
            with output_path.open("w", encoding="utf-8") as output_file:
                output_file.write(content)
            logger.info(f"Output file created: {output_path}")
        except IOError as e:
            logger.error(f"Error writing to output file: {e}")
    else:
        rprint(Panel(Syntax(content, "markdown", theme="monokai", line_numbers=True)))


def log_token_count(count: int):
    """
    Log the total number of tokens processed.

    Args:
        count (int): The total number of tokens processed.
    """
    rprint(f"[cyan]🔢 Token count: {count}[/cyan]")


def log_clipboard_copy(success: bool = True):
    """
    Log whether the content was successfully copied to the clipboard.

    Args:
        success (bool): Indicates whether the content was successfully copied to the clipboard.
    """
    if success:
        rprint("[green]📋 Content copied to clipboard[/green]")
    else:
        rprint("[yellow]📋 Failed to copy content to clipboard[/yellow]")