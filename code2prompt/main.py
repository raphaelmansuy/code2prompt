import click
from pathlib import Path
import tiktoken
from code2prompt.utils.is_binary import is_binary
from code2prompt.utils.generate_markdown_content import generate_markdown_content
from code2prompt.utils.is_filtered import is_filtered
from code2prompt.utils.is_ignored import is_ignored
from code2prompt.utils.parse_gitignore import parse_gitignore
from code2prompt.process_file import process_file
from code2prompt.write_output import write_output
from code2prompt.template_processor import load_template, process_template, get_user_inputs

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

def get_gitignore_patterns(path, gitignore):
    """
    Retrieve gitignore patterns from a specified path or a default .gitignore file.

    This function reads the .gitignore file located at the specified path or uses
    the default .gitignore file in the project root if no specific path is provided.
    It then parses the file to extract ignore patterns and adds a default pattern
    to ignore the .git directory itself.

    Args:
        path (Path): The root path of the project where the default .gitignore file is located.
        gitignore (Optional[str]): An optional path to a specific .gitignore file to use instead of the default.

    Returns:
        Set[str]: A set of gitignore patterns extracted from the .gitignore file.
    """
    gitignore_path = Path(gitignore) if gitignore else path / ".gitignore"
    patterns = parse_gitignore(gitignore_path)
    patterns.add(".git")
    return patterns

def should_process_file(file_path, gitignore_patterns, root_path, options):
    """
    Determine whether a file should be processed based on several criteria.

    Checks if the file is indeed a file, not ignored according to gitignore patterns,
    matches the filter criteria, is not excluded, is case sensitive if specified,
    and is not a binary file.

    Args:
        file_path (Path): The path to the file being considered.
        gitignore_patterns (set): A set of patterns to ignore files.
        root_path (Path): The root path of the project for relative comparisons.
        options (dict): A dictionary of options including filter, exclude, and case sensitivity settings.

    Returns:
        bool: True if the file should be processed, False otherwise.
    """
    return (
        file_path.is_file()
        and not is_ignored(file_path, gitignore_patterns, root_path)
        and is_filtered(file_path, options['filter'], options['exclude'], options['case_sensitive'])
        and not is_binary(file_path)
    )

def generate_content(files_data, options):
    """
    Generate content based on the provided files data and options.

    This function either processes a Jinja2 template with the given files data and user inputs
    or generates markdown content directly from the files data, depending on whether a
    template option is provided.

    Args:
        files_data (list): A list of dictionaries containing processed file data.
        options (dict): A dictionary containing options such as template path and whether
                        to wrap code inside markdown code blocks.

    Returns:
        str: The generated content as a string, either from processing a template or
             directly generating markdown content.
    """
    if options['template']:
        template_content = load_template(options['template'])
        user_inputs = get_user_inputs(template_content)
        return process_template(template_content, files_data, user_inputs)
    return generate_markdown_content(files_data, options['no_codeblock'])

def count_tokens(text: str, encoding: str) -> int:
    """
    Count the number of tokens in the given text using the specified encoding.

    Args:
        text (str): The text to tokenize and count.
        encoding (str): The encoding to use for tokenization.

    Returns:
        int: The number of tokens in the text.
    """
    try:
        encoder = tiktoken.get_encoding(encoding)
        return len(encoder.encode(text))
    except Exception as e:
        click.echo(f"Error counting tokens: {str(e)}", err=True)
        return 0

if __name__ == "__main__":
    # pylint: disable=no-value-for-parameter
    create_markdown_file()