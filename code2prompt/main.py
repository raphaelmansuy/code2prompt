""" Main module for the code2prompt package. """

from datetime import datetime
from pathlib import Path
from fnmatch import fnmatch
import click

from code2prompt.language_inference import infer_language
from code2prompt.comment_stripper import strip_comments


def parse_gitignore(gitignore_path):
    """Parse the .gitignore file and return a set of patterns."""
    if not gitignore_path.exists():
        return set()

    with gitignore_path.open("r", encoding="utf-8") as file:
        patterns = set(
            line.strip() for line in file if line.strip() and not line.startswith("#")
        )
    return patterns


def is_ignored(file_path: Path, gitignore_patterns: list, base_path: Path) -> bool:
    """
    Check if a file path matches any pattern in the .gitignore file.

    Args:
        file_path (Path): The path of the file being checked.
        gitignore_patterns (list): A list of patterns from the .gitignore file.
        base_path (Path): The base path of the repository.

    Returns:
        bool: True if the file path matches any pattern, False otherwise.
    """
    relative_path = file_path.relative_to(base_path)

    for pattern in gitignore_patterns:
        pattern = pattern.rstrip("/")  # Remove trailing slash from the pattern

        if pattern.startswith("/"):
            if fnmatch(str(relative_path), pattern[1:]):
                return True
            if fnmatch(str(relative_path.parent), pattern[1:]):
                return True
        else:
            for path in relative_path.parents:
                if fnmatch(str(path / relative_path.name), pattern):
                    return True
                if fnmatch(str(path), pattern):
                    return True
            if fnmatch(str(relative_path), pattern):
                return True

    return False


def is_filtered(file_path, filter_pattern):
    """Check if a file path matches the filter pattern."""
    return fnmatch(file_path.name, filter_pattern)


def is_binary(file_path):
    """
    Determines if the specified file is a binary file.

    Args:
    file_path (str): The path to the file to check.

    Returns:
    bool: True if the file is binary, False otherwise.
    """
    try:
        with open(file_path, "rb") as file:
            # Read a small portion of the file
            chunk = file.read(1024)
            # A file is considered binary if it contains a null byte
            return b"\x00" in chunk
    except IOError:
        # Handle the exception if the file cannot be opened
        print(f"Error: The file at {file_path} could not be opened.")
        return False


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
    "--filter", "-f", type=str, help='Filter pattern to include files (e.g., "*.py").'
)
@click.option(
    "--suppress-comments",
    "-s",
    is_flag=True,
    help="Strip comments from the code files.",
    default=False,
)
def create_markdown_file(path, output, gitignore, filter, suppress_comments):
    """Create a Markdown file with the content of files in a directory."""
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
            and (not filter or is_filtered(file_path, filter))
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
                # Ignore files that cannot be decoded
                continue

            file_info = f"## File: {file_path}\n\n"
            file_info += f"- Extension: {file_extension}\n"
            file_info += f"- Size: {file_size} bytes\n"
            file_info += f"- Created: {file_creation_time}\n"
            file_info += f"- Modified: {file_modification_time}\n\n"

            language = infer_language(file_path.name)
            if language == "unknown":
                language = format(file_extension[1:])

            file_code = f"### Code\n```{language}\n{file_content}\n```\n\n"

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
    create_markdown_file()
