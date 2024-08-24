# code2prompt/main.py

from pathlib import Path
import click

from code2prompt.config import Configuration
from code2prompt.commands.generate import GenerateCommand
from code2prompt.commands.analyze import AnalyzeCommand
from code2prompt.print_help import print_help
from code2prompt.utils.logging_utils import setup_logger
from code2prompt.version import VERSION


@click.group(invoke_without_command=True)
@click.version_option(
    VERSION, "-v", "--version", message="code2prompt version %(version)s"
)
@click.option(
    "--config",
    type=click.Path(exists=True, dir_okay=False),
    help="Path to configuration file",
)
@click.pass_context
def cli(ctx, config):
    """code2prompt CLI tool

    This command-line interface (CLI) tool allows users to generate prompts from codebases,
    analyze code structure, and manage configurations. It provides various options for customizing
    the output and behavior of the tool.

    Args:
        ctx: The Click context object.
        config: Optional path to a configuration file.
    """
    ctx.obj = {}
    if config:
        ctx.obj["config"] = Configuration.load_from_file(Path(config))
    else:
        ctx.obj["config"] = Configuration()

    if ctx.invoked_subcommand is None:
        print_help(ctx)


@cli.command()
@click.option(
    "--path",
    "-p",
    type=click.Path(exists=True),
    multiple=True,
    help="Path(s) to the directory or file to process.",
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
)
@click.option(
    "--line-number", "-ln", is_flag=True, help="Add line numbers to source code blocks."
)
@click.option(
    "--no-codeblock",
    is_flag=True,
    help="Disable wrapping code inside markdown code blocks.",
)
@click.option(
    "--template",
    "-t",
    type=click.Path(exists=True),
    help="Path to a Jinja2 template file for custom prompt generation.",
)
@click.option(
    "--tokens", is_flag=True, help="Display the token count of the generated prompt."
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
        ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"], case_sensitive=False
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
    "--provider", type=str, help="Specify the provider for price calculation."
)
@click.option("--model", type=str, help="Specify the model for price calculation.")
@click.option(
    "--output-tokens",
    type=int,
    default=1000,
    help="Specify the number of output tokens for price calculation.",
)
@click.pass_context
def generate(ctx, **options):
    """Generate markdown from code files

    This command processes the specified code files or directories and generates a Markdown
    output file containing prompts based on the code structure and content.

    Args:
        ctx: The Click context object.
        options: Various options for customizing the generation process.
    """
    config = ctx.obj["config"].merge(options)
    logger = setup_logger(level=config.log_level)

    # if config.create_templates:
    #    create_templates_directory()
    #    return

    command = GenerateCommand(config, logger)
    command.execute()


@cli.command()
@click.option(
    "--path",
    "-p",
    type=click.Path(exists=True),
    multiple=True,
    help="Path(s) to analyze.",
)
@click.option(
    "--format",
    type=click.Choice(["flat", "tree"]),
    default="flat",
    help="Format of the analysis output.",
)
@click.pass_context
def analyze(ctx, **options):
    """Analyze codebase structure

    This command analyzes the structure of the specified codebase and provides an output
    in either a flat or tree-like format, summarizing the files and their relationships.

    Args:
        ctx: The Click context object.
        options: Various options for customizing the analysis output.
    """
    config = ctx.obj["config"].merge(options)
    logger = setup_logger(level=config.log_level)
    command = AnalyzeCommand(config, logger)
    command.execute()


if __name__ == "__main__":
    cli(standalone_mode=False)
