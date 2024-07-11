from importlib import resources
import logging
from pathlib import Path
import click
from tabulate import tabulate
from code2prompt.utils.config import load_config, merge_options
from code2prompt.utils.count_tokens import count_tokens
from code2prompt.core.generate_content import generate_content
from code2prompt.core.process_files import process_files
from code2prompt.core.write_output import write_output
from code2prompt.utils.create_template_directory import create_templates_directory
from code2prompt.utils.logging_utils import setup_logger, log_token_count, log_error, log_info
from code2prompt.utils.price_calculator import load_token_prices, calculate_prices

VERSION = "0.6.10"

DEFAULT_OPTIONS = {
    "path": [],
    "output": None,
    "gitignore": None,
    "filter": None,
    "exclude": None,
    "case_sensitive": False,
    "suppress_comments": False,
    "line_number": False,
    "no_codeblock": False,
    "template": None,
    "tokens": False,
    "encoding": "cl100k_base",
    "create_templates": False,
    "log_level": "INFO",
    "price": False,
    "provider": None,
    "model": None,
    "output_tokens": 1000,  # Default output token count
}

@click.command()
@click.version_option(
    VERSION, "-v", "--version", message="code2prompt version %(version)s"
)
@click.option(
    "--path", "-p",
    type=click.Path(exists=True),
    multiple=True,
    help="Path(s) to the directory or file to process.",
)
@click.option(
    "--output", "-o",
    type=click.Path(),
    help="Name of the output Markdown file."
)
@click.option(
    "--gitignore", "-g",
    type=click.Path(exists=True),
    help="Path to the .gitignore file.",
)
@click.option(
    "--filter", "-f",
    type=str,
    help='Comma-separated filter patterns to include files (e.g., "*.py,*.js").',
)
@click.option(
    "--exclude", "-e",
    type=str,
    help='Comma-separated patterns to exclude files (e.g., "*.txt,*.md").',
)
@click.option(
    "--case-sensitive",
    is_flag=True,
    help="Perform case-sensitive pattern matching."
)
@click.option(
    "--suppress-comments", "-s",
    is_flag=True,
    help="Strip comments from the code files.",
    default=False,
)
@click.option(
    "--line-number", "-ln",
    is_flag=True,
    help="Add line numbers to source code blocks.",
    default=False,
)
@click.option(
    "--no-codeblock",
    is_flag=True,
    help="Disable wrapping code inside markdown code blocks.",
)
@click.option(
    "--template", "-t",
    type=click.Path(exists=True),
    help="Path to a Jinja2 template file for custom prompt generation.",
)
@click.option(
    "--tokens",
    is_flag=True,
    help="Display the token count of the generated prompt."
)
@click.option(
    "--encoding",
    type=click.Choice(["cl100k_base", "p50k_base", "p50k_edit", "r50k_base"]),
    default="cl100k_base",
    help="Specify the tokenizer encoding to use.",
)
@click.option(
    "--create-templates",
    is_flag=True,
    help="Create a templates directory with example templates.",
)
@click.option(
    "--log-level",
    type=click.Choice(
        ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        case_sensitive=False
    ),
    default="INFO",
    help="Set the logging level.",
)
@click.option(
    "--price",
    is_flag=True,
    help="Display the estimated price of tokens based on provider and model.",
)
@click.option(
    "--provider",
    type=str,
    help="Specify the provider for price calculation.",
)
@click.option(
    "--model",
    type=str,
    help="Specify the model for price calculation.",
)
@click.option(
    "--output-tokens",
    type=int,
    default=1000,
    help="Specify the number of output tokens for price calculation.",
)
def create_markdown_file(**cli_options):
    """
    Creates a Markdown file based on the provided options.

    This function orchestrates the process of reading files from the specified paths,
    processing them according to the given options (such as filtering, excluding certain files,
    handling comments, etc.), and then generating a Markdown file with the processed content.
    The output file name and location can be customized through the options.

    Args:
        **options (dict): Key-value pairs of options to customize the behavior of the function.
        Possible keys include 'path', 'output', 'gitignore', 'filter', 'exclude', 'case_sensitive',
        'suppress_comments', 'line_number', 'no_codeblock', 'template', 'tokens', 'encoding',
        'create_templates', 'log_level', 'price', 'provider', 'model', and 'output_tokens'.

    Returns:
        None
    """
    # Load configuration from .code2promptrc files
    config = load_config(".")

    # Merge options: CLI takes precedence over config, which takes precedence over defaults
    options = merge_options(cli_options, config, DEFAULT_OPTIONS)

    # Set up logger with the specified log level
    _logger = setup_logger(level=getattr(logging, options["log_level"].upper()))

    if options["create_templates"]:
        cwd = Path.cwd()
        templates_dir = cwd / "templates"
        package_templates_dir = resources.files("code2prompt").joinpath("templates")
        create_templates_directory(
            package_templates_dir=package_templates_dir,
            templates_dir=templates_dir
        )
        return

    if not options["path"]:
        log_error(
            "Error: No path specified. Please provide a path using --path option or in .code2promptrc file."
        )
        return

    all_files_data = []
    for path in options["path"]:
        files_data = process_files({**options, "path": path})
        all_files_data.extend(files_data)

    content = generate_content(all_files_data, options)

    token_count = None
    if options["tokens"] or options["price"]:
        token_count = count_tokens(content, options["encoding"])
        log_token_count(token_count)


    write_output(content, options["output"], copy_to_clipboard=True)
    
    if options["price"]:
        display_price_table(options, token_count)


def display_price_table(options, token_count):
    """
    Display a table with price estimates for the given token count.

    Args:
        options (dict): The options dictionary containing pricing-related settings.
        token_count (int): The number of tokens to calculate prices for.
    """
    if token_count is None:
        log_error("Error: Token count is required for price calculation.")
        return

    token_prices = load_token_prices()
    if not token_prices:
        return

    output_token_count = options["output_tokens"]

    table_data = calculate_prices(token_prices, token_count, output_token_count, options["provider"], options["model"])

    if not table_data:
        log_error("Error: No matching provider or model found")
        return

    headers = ["Provider", "Model", "Price for 1K Input Tokens", "Number of Input Tokens", "Total Price"]
    table = tabulate(table_data, headers=headers, tablefmt="grid")
    log_info("\n✨ Estimated Token Prices: (All prices are in USD, it is an estimate as the current token implementation is based on OpenAI's GPT-3)")
    log_info("\n")
    log_info(table)
    log_info("\n📝 Note: The prices are based on the token count and the provider's pricing model.")

if __name__ == "__main__":
    create_markdown_file()