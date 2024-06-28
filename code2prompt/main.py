from pathlib import Path
import click
from code2prompt.file_handling import (
    parse_gitignore,
    is_ignored,
    is_filtered,
    is_binary
)
from code2prompt.generate_markdown_content import generate_markdown_content
from code2prompt.process_file import process_file
from code2prompt.write_output import write_output

@click.command()
@click.option("--path", "-p", type=click.Path(exists=True), required=True, help="Path to the directory to navigate.")
@click.option("--output", "-o", type=click.Path(), help="Name of the output Markdown file.")
@click.option("--gitignore", "-g", type=click.Path(exists=True), help="Path to the .gitignore file.")
@click.option("--filter", "-f", type=str, help='Comma-separated filter patterns to include files (e.g., "*.py,*.js").')
@click.option("--exclude", "-e", type=str, help='Comma-separated patterns to exclude files (e.g., "*.txt,*.md").')
@click.option("--case-sensitive", is_flag=True, help="Perform case-sensitive pattern matching.")
@click.option("--suppress-comments", "-s", is_flag=True, help="Strip comments from the code files.", default=False)
@click.option("--line-number", "-ln", is_flag=True, help="Add line numbers to source code blocks.", default=False)
def create_markdown_file(path, output, gitignore, filter, exclude, suppress_comments, case_sensitive, line_number):
    path = Path(path)
    gitignore_path = Path(gitignore) if gitignore else path / ".gitignore"
    gitignore_patterns = parse_gitignore(gitignore_path)
    gitignore_patterns.add(".git")

    files_data = []
    for file_path in path.rglob("*"):
        if (
            file_path.is_file()
            and not is_ignored(file_path, gitignore_patterns, path)
            and is_filtered(file_path, filter, exclude, case_sensitive)
            and not is_binary(file_path)
        ):
            result = process_file(file_path, suppress_comments, line_number)
            if result:
                files_data.append(result)

    markdown_content = generate_markdown_content(files_data)
    write_output(markdown_content, output)

if __name__ == "__main__":
    # pylint: disable=no-value-for-parameter
    # pylint: disable=E1120
    create_markdown_file()