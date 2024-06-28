from datetime import datetime
from pathlib import Path
import click
from code2prompt.language_inference import infer_language
from code2prompt.comment_stripper import strip_comments
from code2prompt.file_handling import (
    parse_gitignore,
    is_ignored,
    is_filtered,
    is_binary,
)


@click.command()
@click.option(
    "--path",
    "-p",
    type=click.Path(exists=True),
    required=True,
    help="Path to the directory to navigate.",
)
@click.option(
    "--output", "-o", type=click.Path(), help="Name of the output Markdown file."
)
@click.option(
    "--gitignore",
    "-g",
    type=click.Path(exists=True),
    help="Path to the .gitignore file.",
)
@click.option(
    "--filter",
    "-f",
    type=str,
    help='Comma-separated filter patterns to include files (e.g., "*.py,*.js").',
)
@click.option(
    "--exclude",
    "-e",
    type=str,
    help='Comma-separated patterns to exclude files (e.g., "*.txt,*.md").',
)
@click.option(
    "--case-sensitive", is_flag=True, help="Perform case-sensitive pattern matching."
)
@click.option(
    "--suppress-comments",
    "-s",
    is_flag=True,
    help="Strip comments from the code files.",
    default=False,
)
def create_markdown_file(
    path, output, gitignore, filter, exclude, suppress_comments, case_sensitive
):
    content = []
    table_of_contents = []
    path = Path(path)
    gitignore_path = Path(gitignore) if gitignore else path / ".gitignore"
    gitignore_patterns = parse_gitignore(gitignore_path)
    gitignore_patterns.add(".git")

    for file_path in path.rglob("*"):
        if (
            file_path.is_file()
            and not is_ignored(file_path, gitignore_patterns, path)
            and is_filtered(file_path, filter, exclude, case_sensitive)
            and not is_binary(file_path)
        ):
            file_extension = file_path.suffix
            file_size = file_path.stat().st_size
            file_creation_time = datetime.fromtimestamp(
                file_path.stat().st_ctime
            ).strftime("%Y-%m-%d %H:%M:%S")
            file_modification_time = datetime.fromtimestamp(
                file_path.stat().st_mtime
            ).strftime("%Y-%m-%d %H:%M:%S")

            try:
                with file_path.open("r", encoding="utf-8") as f:
                    file_content = f.read()
                    if suppress_comments:
                        language = infer_language(file_path.name)
                        if language != "unknown":
                            file_content = strip_comments(file_content, language)
            except UnicodeDecodeError:
                continue

            file_info = f"## File: {file_path}\n\n"
            file_info += f"- Extension: {file_extension}\n"
            file_info += f"- Size: {file_size} bytes\n"
            file_info += f"- Created: {file_creation_time}\n"
            file_info += f"- Modified: {file_modification_time}\n\n"
            file_code = f"### Code\n\n\n"
            content.append(file_info + file_code)
            table_of_contents.append(
                f"- [{file_path}](#{file_path.as_posix().replace('/', '')})\n"
            )

    markdown_content = (
        "# Table of Contents\n" + "".join(table_of_contents) + "\n" + "".join(content)
    )
    if output:
        output_path = Path(output)
        with output_path.open("w", encoding="utf-8") as md_file:
            md_file.write(markdown_content)
        click.echo(f"Markdown file '{output_path}' created successfully.")
    else:
        click.echo(markdown_content)


if __name__ == "__main__":
    # pylint: disable=no-value-for-parameter
    # pylint: disable=E1120
    create_markdown_file()
