"""Main module for the code2prompt CLI tool."""

import logging
from pathlib import Path
import click
from code2prompt.commands.analyze import AnalyzeCommand
from code2prompt.commands.generate import GenerateCommand
from code2prompt.config import Configuration
from code2prompt.utils.logging_utils import setup_logger
from code2prompt.commands.interactive_selector import InteractiveFileSelector
from code2prompt.core.file_path_retriever import retrieve_file_paths
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
    "--interactive",
    "-i",
    is_flag=True,
    help="Interactive mode to select files.",
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
    default="WARNING",
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
def cli(ctx, config, path, **generate_options):
    """code2prompt CLI tool"""
    ctx.obj = {}
    if config:
        ctx.obj["config"] = Configuration.load_from_file(Path(config))
    else:
        ctx.obj["config"] = Configuration()

    logging.info("CLI initialized with config: %s", ctx.obj["config"])

    if ctx.invoked_subcommand is None:
        ctx.invoke(generate, path=path, **generate_options)


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
@click.pass_context
def generate(ctx, **options):
    """Generate markdown from code files"""

    config = ctx.obj["config"].merge(options)
    logger = setup_logger(level=config.log_level)

    selected_paths: list[Path] = [Path(p) for p in config.path]

    # Check if selected_paths is empty before proceeding
    if not selected_paths:
        logging.error("No file paths provided. Please specify valid paths.")
        return  # Exit the function if no paths are provided

    filter_patterns: list[str] = config.filter.split(",") if config.filter else []
    exclude_patterns: list[str] = config.exclude.split(",") if config.exclude else []
    case_sensitive: bool = config.case_sensitive
    gitignore: str = config.gitignore

    # Handle both directory and file inputs
    filtered_paths = []
    for path in selected_paths:
        if path.is_dir():
            filtered_paths.extend(retrieve_file_paths(
                file_paths=[path],
                gitignore=gitignore,
                filter_patterns=filter_patterns,
                exclude_patterns=exclude_patterns,
                case_sensitive=case_sensitive,
            ))
        elif path.is_file():
            filtered_paths.append(path)

    if filtered_paths and config.interactive:
        file_selector = InteractiveFileSelector(filtered_paths, filtered_paths)
        filtered_selected_path = file_selector.run()
        config.path = filtered_selected_path
    else:
        config.path = filtered_paths

    command = GenerateCommand(config, logger)
    command.execute()

    logger.info("Markdown generation completed.")


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
    """Analyze codebase structure"""
    config = ctx.obj["config"].merge(options)
    logger = setup_logger(level=config.log_level)
    logger.info("Analyzing codebase with options: %s", options)

    command = AnalyzeCommand(config, logger)
    command.execute()

    logger.info("Codebase analysis completed.")


def get_directory_tree(path):
    """Retrieve a list of files and directories in a given path."""
    return [p.name for p in Path(path).iterdir() if p.is_file() or p.is_dir()]
