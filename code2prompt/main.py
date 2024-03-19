import os
import click
from datetime import datetime
from pathlib import Path
from fnmatch import fnmatch
import mimetypes

def parse_gitignore(gitignore_path):
    """Parse the .gitignore file and return a set of patterns."""
    if not gitignore_path.exists():
        return set()

    with gitignore_path.open('r', encoding='utf-8') as file:
        patterns = set(line.strip() for line in file if line.strip() and not line.startswith('#'))
    return patterns

def is_ignored(file_path, gitignore_patterns, base_path):
    """Check if a file path matches any pattern in the .gitignore file."""
    relative_path = file_path.relative_to(base_path)
    for pattern in gitignore_patterns:
        if relative_path.match(pattern):
            return True
        if file_path.name == pattern:
            return True
        if str(relative_path).startswith(pattern + '/'):
            return True
        if fnmatch(str(relative_path), pattern) or fnmatch(str(file_path), pattern):
            return True
    return False

def is_filtered(file_path, filter_pattern):
    """Check if a file path matches the filter pattern."""
    return fnmatch(file_path.name, filter_pattern)

def is_binary(file_path):
    """Check if a file is binary."""
    mime_type, _ = mimetypes.guess_type(file_path)
    return mime_type is not None and not mime_type.startswith('text')

@click.command()
@click.option('--path', '-p', type=click.Path(exists=True), required=True,
              help='Path to the directory to navigate.')
@click.option('--output', '-o', type=click.Path(),
              help='Name of the output Markdown file.')
@click.option('--gitignore', '-g', type=click.Path(exists=True),
              help='Path to the .gitignore file.')
@click.option('--filter', '-f', type=str,
              help='Filter pattern to include files (e.g., "*.py").')
def create_markdown_file(path, output, gitignore, filter):
    """Create a Markdown file with the content of files in a directory."""
    content = []
    table_of_contents = []

    path = Path(path)
    gitignore_path = Path(gitignore) if gitignore else path / '.gitignore'
    gitignore_patterns = parse_gitignore(gitignore_path)

    for file_path in path.rglob('*'):
        if (
            file_path.is_file()
            and not is_ignored(file_path, gitignore_patterns, path)
            and (not filter or is_filtered(file_path, filter))
            and not is_binary(file_path)
        ):
            file_extension = file_path.suffix
            file_size = file_path.stat().st_size
            file_creation_time = datetime.fromtimestamp(file_path.stat().st_ctime).strftime('%Y-%m-%d %H:%M:%S')
            file_modification_time = datetime.fromtimestamp(file_path.stat().st_mtime).strftime('%Y-%m-%d %H:%M:%S')

            try:
                with file_path.open('r', encoding='utf-8') as f:
                    file_content = f.read()
            except UnicodeDecodeError:
                click.echo(f"Skipping file '{file_path}' due to encoding issues.")
                continue

            file_info = f"## File: {file_path}\n\n"
            file_info += f"- Extension: {file_extension}\n"
            file_info += f"- Size: {file_size} bytes\n"
            file_info += f"- Created: {file_creation_time}\n"
            file_info += f"- Modified: {file_modification_time}\n\n"

            file_summary = "### Summary\n"
            file_summary += "This file contains the implementation of...\n\n"

            file_code = f"### Code\n```{file_extension}\n{file_content}\n```\n\n"

            content.append(file_info + file_summary + file_code)
            table_of_contents.append(f"- [{file_path}](#{file_path.as_posix().replace('/', '')})\n")

    markdown_content = "# Table of Contents\n" + ''.join(table_of_contents) + "\n" + ''.join(content)

    if output:
        output_path = Path(output)
        with output_path.open('w', encoding='utf-8') as md_file:
            md_file.write(markdown_content)
        click.echo(f"Markdown file '{output_path}' created successfully.")
    else:
        click.echo(markdown_content)

if __name__ == '__main__':
    create_markdown_file()