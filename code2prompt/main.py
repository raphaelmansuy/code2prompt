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


class Code2PromptGroup(click.Group):
    """Click group that tolerates stray positional arguments.

    Shells expand unquoted globs before click sees them, so
    ``code2prompt --path . --filter **.py`` can arrive as
    ``code2prompt --path . --filter core_rag.py utils.py ...``: the first
    expanded filename is swallowed as the --filter value and the next one is
    mistaken for a subcommand name ("No such command 'core_rag.py'").
    When the unknown word is an existing file or directory, treat all of the
    stray arguments as extra input paths for ``generate`` instead of failing;
    anything else keeps click's normal "No such command" error.
    """

    def resolve_command(self, ctx, args):
        try:
            return super().resolve_command(ctx, args)
        except click.UsageError:
            if args and Path(args[0]).exists():
                # Mark the fallback on the context: the group callback runs
                # next and must hand its own options to `generate`, because
                # the subcommand only sees the stray arguments.
                ctx._code2prompt_stray_paths = True
                cmd = self.get_command(ctx, "generate")
                return "generate", cmd, args
            raise


@click.group(cls=Code2PromptGroup, invoke_without_command=True)
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
@click.option(
    "--syntax-map",
    type=str,
    help="Comma-separated list of extension:synonym mappings for syntax highlighting."
)
@click.pass_context
def cli(ctx, config, path, **generate_options):
    """code2prompt CLI tool"""
    ctx.obj = {}
    if config:
        ctx.obj["config"] = Configuration.load_from_file(Path(config))
    else:
        ctx.obj["config"] = Configuration()  # This will now have syntax_map initialized

    logging.info("CLI initialized with config: %s", ctx.obj["config"])

    if ctx.invoked_subcommand is None:
        ctx.invoke(generate, path=path, **generate_options)
    elif getattr(ctx, "_code2prompt_stray_paths", False):
        # The stray arguments were dispatched to `generate` as extra paths,
        # but that subcommand only parses the stray arguments themselves.
        # Hand it the group-level options (e.g. --path/--filter given before
        # the stray filenames) via ctx.obj; `generate` merges them in.
        ctx.obj["_fallback_generate"] = {"path": path, **generate_options}


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
@click.argument("extra_paths", nargs=-1, type=click.Path(exists=True))
@click.pass_context
def generate(ctx, **options):
    """Generate markdown from code files"""

    # Stray positional arguments (e.g. filenames from a shell-expanded glob
    # such as an unquoted --filter **.py) are treated as extra input paths.
    # They must not reach Configuration.merge (unknown key) and are merged
    # into the input paths below.
    extra_paths = options.pop("extra_paths", ())

    # Fallback from Code2PromptGroup.resolve_command (stray positional
    # arguments, e.g. filenames from a shell-expanded glob): the group-level
    # options given before them are stashed in ctx.obj. Merge them in where
    # the subcommand did not receive its own value for that option.
    if ctx.obj:
        fallback = ctx.obj.pop("_fallback_generate", None)
        if fallback:
            for key, value in fallback.items():
                current = options.get(key)
                if current is None or current in ((), [], "", {}):
                    options[key] = value

    # Parse the syntax_map option into a dictionary
    if options.get('syntax_map'):
        syntax_map = {}
        for mapping in options['syntax_map'].split(','):
            ext, syntax = mapping.split(':')
            syntax_map['.' + ext.strip()] = syntax.strip()  # Add a dot before the extension
        options['syntax_map'] = syntax_map  # Replace the string with the dictionary

    config = ctx.obj["config"].merge(options)
    logger = setup_logger(level=config.log_level)

    if extra_paths:
        logger.warning(
            "Treating unexpected argument(s) as additional input path(s): %s. "
            "If your shell expanded an unquoted glob, quote filter patterns "
            "(e.g. --filter \"**.py\").",
            ", ".join(extra_paths),
        )

    selected_paths: list[Path] = [Path(p) for p in config.path]
    selected_paths.extend(Path(p) for p in extra_paths)

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

    # The same file can arrive twice (e.g. once via --path . and once as a
    # shell-expanded stray argument); keep each file only once, in order.
    filtered_paths = list(dict.fromkeys(filtered_paths))

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
