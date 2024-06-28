import click
from pathlib import Path
from code2prompt.count_tokens import count_tokens
from code2prompt.generate_content import generate_content
from code2prompt.get_gitignore_patterns import get_gitignore_patterns
from code2prompt.should_process_file import should_process_file
from code2prompt.process_file import process_file
from code2prompt.write_output import write_output

VERSION = "0.5.0" # Define the version of the CLI tool

@click.command()
@click.version_option(VERSION, '-v', '--version', message='code2prompt version %(version)s')
@click.option("--path", "-p", type=click.Path(exists=True), required=True, help="Path to the directory to navigate.")
@click.option("--output", "-o", type=click.Path(), help="Name of the output Markdown file.")
@click.option("--gitignore", "-g", type=click.Path(exists=True), help="Path to the .gitignore file.")
@click.option("--filter", "-f", type=str, help='Comma-separated filter patterns to include files (e.g., "*.py,*.js").')
@click.option("--exclude", "-e", type=str, help='Comma-separated patterns to exclude files (e.g., "*.txt,*.md").')
@click.option("--case-sensitive", is_flag=True, help="Perform case-sensitive pattern matching.")
@click.option("--suppress-comments", "-s", is_flag=True, help="Strip comments from the code files.", default=False)
@click.option("--line-number", "-ln", is_flag=True, help="Add line numbers to source code blocks.", default=False)
@click.option("--no-codeblock", is_flag=True, help="Disable wrapping code inside markdown code blocks.")
@click.option("--template", "-t", type=click.Path(exists=True), help="Path to a Jinja2 template file for custom prompt generation.")
@click.option("--tokens", is_flag=True, help="Display the token count of the generated prompt.")
@click.option("--encoding", type=click.Choice(['cl100k_base', 'p50k_base', 'p50k_edit', 'r50k_base']), 
              default='cl100k_base', help="Specify the tokenizer encoding to use.")
def create_markdown_file(**options):
    """
    Creates a Markdown file based on the provided options.

    This function orchestrates the process of reading files from the specified path,
    processing them according to the given options (such as filtering, excluding certain files,
    handling comments, etc.), and then generating a Markdown file with the processed content.
    The output file name and location can be customized through the options.

    Args:
        **options (dict): Key-value pairs of options to customize the behavior of the function.
                          Possible keys include 'path', 'output', 'gitignore', 'filter', 'exclude',
                          'case_sensitive', 'suppress_comments', 'line_number', 'no_codeblock',
                          'template', 'tokens', and 'encoding'.

    Returns:
        None
    """
    files_data = process_files(options)
    content = generate_content(files_data, options)
    
    if options['tokens']:
        token_count = count_tokens(content, options['encoding'])
        click.echo(f"Token count: {token_count}")
    
    write_output(content, options['output'])

def process_files(options):
    """
    Processes files within a specified directory, applying filters and transformations
    based on the provided options.

    Args:
        options (dict): A dictionary containing options such as path, gitignore patterns,
                        and flags for processing files.

    Returns:
        list: A list of dictionaries containing processed file data.
    """
    path = Path(options['path'])
    gitignore_patterns = get_gitignore_patterns(path, options['gitignore'])
    files_data = []
    for file_path in path.rglob("*"):
        if should_process_file(file_path, gitignore_patterns, path, options):
            result = process_file(file_path, options['suppress_comments'], options['line_number'], options['no_codeblock'])
            if result:
                files_data.append(result)
    return files_data

if __name__ == "__main__":
    # pylint: disable=no-value-for-parameter
    create_markdown_file()