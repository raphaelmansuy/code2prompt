import logging
from pathlib import Path
import click
from prompt_toolkit import Application
from prompt_toolkit.layout.containers import VSplit, HSplit, Window, ScrollablePane, Frame
from prompt_toolkit.layout.controls import FormattedTextControl
from prompt_toolkit.layout.layout import Layout
from prompt_toolkit.widgets import CheckboxList
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.formatted_text import HTML
from code2prompt.commands.analyze import AnalyzeCommand
from code2prompt.commands.generate import GenerateCommand
from code2prompt.config import Configuration
from code2prompt.utils.logging_utils import setup_logger
from code2prompt.version import VERSION

@click.group(invoke_without_command=True)
@click.version_option(VERSION, "-v", "--version", message="code2prompt version %(version)s")
@click.option("--config", type=click.Path(exists=True, dir_okay=False), help="Path to configuration file")
@click.option("--path", "-p", type=click.Path(exists=True), multiple=True, help="Path(s) to the directory or file to process.")
@click.option("--output", "-o", type=click.Path(), help="Name of the output Markdown file.")
@click.option("--gitignore", "-g", type=click.Path(exists=True), help="Path to the .gitignore file.")
@click.option("--filter", "-f", type=str, help='Comma-separated filter patterns to include files (e.g., "*.py,*.js").')
@click.option("--exclude", "-e", type=str, help='Comma-separated patterns to exclude files (e.g., "*.txt,*.md").')
@click.option("--case-sensitive", is_flag=True, help="Perform case-sensitive pattern matching.")
@click.option("--suppress-comments", "-s", is_flag=True, help="Strip comments from the code files.")
@click.option("--line-number", "-ln", is_flag=True, help="Add line numbers to source code blocks.")
@click.option("--no-codeblock", is_flag=True, help="Disable wrapping code inside markdown code blocks.")
@click.option("--template", "-t", type=click.Path(exists=True), help="Path to a Jinja2 template file for custom prompt generation.")
@click.option("--tokens", is_flag=True, help="Display the token count of the generated prompt.")
@click.option("--encoding", type=click.Choice(["cl100k_base", "p50k_base", "p50k_edit", "r50k_base"]), default="cl100k_base", help="Specify the tokenizer encoding to use.")
@click.option("--create-templates", is_flag=True, help="Create a templates directory with example templates.")
@click.option("--log-level", type=click.Choice(["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"], case_sensitive=False), default="WARNING", help="Set the logging level.")
@click.option("--price", is_flag=True, help="Display the estimated price of tokens based on provider and model.")
@click.option("--provider", type=str, help="Specify the provider for price calculation.")
@click.option("--model", type=str, help="Specify the model for price calculation.")
@click.option("--output-tokens", type=int, default=1000, help="Specify the number of output tokens for price calculation.")
@click.pass_context
def cli(ctx, config, path, **generate_options):
    """code2prompt CLI tool
    This command-line interface (CLI) tool allows users to generate prompts from codebases, analyze code structure, and manage configurations. It provides various options for customizing the output and behavior of the tool.
    Args:
        ctx: The Click context object.
        config: Optional path to a configuration file.
        path: Path(s) to the directory or file to process.
    """
    ctx.obj = {}
    if config:
        ctx.obj["config"] = Configuration.load_from_file(Path(config))
    else:
        ctx.obj["config"] = Configuration()

    logging.info("CLI initialized with config: %s", ctx.obj["config"])

    if ctx.invoked_subcommand is None:
        ctx.invoke(generate, path=path, **generate_options)  # Pass all generate options

@cli.command()
@click.option("--path", "-p", type=click.Path(exists=True), multiple=True, help="Path(s) to the directory or file to process.")
@click.option("--output", "-o", type=click.Path(), help="Name of the output Markdown file.")
@click.option("--gitignore", "-g", type=click.Path(exists=True), help="Path to the .gitignore file.")
@click.option("--filter", "-f", type=str, help='Comma-separated filter patterns to include files (e.g., "*.py,*.js").')
@click.option("--exclude", "-e", type=str, help='Comma-separated patterns to exclude files (e.g., "*.txt,*.md").')
@click.option("--case-sensitive", is_flag=True, help="Perform case-sensitive pattern matching.")
@click.option("--suppress-comments", "-s", is_flag=True, help="Strip comments from the code files.")
@click.option("--line-number", "-ln", is_flag=True, help="Add line numbers to source code blocks.")
@click.option("--no-codeblock", is_flag=True, help="Disable wrapping code inside markdown code blocks.")
@click.option("--template", "-t", type=click.Path(exists=True), help="Path to a Jinja2 template file for custom prompt generation.")
@click.option("--tokens", is_flag=True, help="Display the token count of the generated prompt.")
@click.option("--encoding", type=click.Choice(["cl100k_base", "p50k_base", "p50k_edit", "r50k_base"]), default="cl100k_base", help="Specify the tokenizer encoding to use.")
@click.option("--create-templates", is_flag=True, help="Create a templates directory with example templates.")
@click.option("--log-level", type=click.Choice(["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"], case_sensitive=False), default="WARNING", help="Set the logging level.")
@click.option("--price", is_flag=True, help="Display the estimated price of tokens based on provider and model.")
@click.option("--provider", type=str, help="Specify the provider for price calculation.")
@click.option("--model", type=str, help="Specify the model for price calculation.")
@click.option("--output-tokens", type=int, default=1000, help="Specify the number of output tokens for price calculation.")
@click.pass_context
def generate(ctx, **options):
    """Generate markdown from code files
    This command processes the specified code files or directories and generates a Markdown output file containing prompts based on the code structure and content.
    Args:
        ctx: The Click context object.
        options: Various options for customizing the generation process.
    """
    config = ctx.obj["config"].merge(options)
    logger = setup_logger(level=config.log_level)
    logger.info("Generating markdown with options: %s", options)

    command = GenerateCommand(config, logger)
    command.execute()

    logger.info("Markdown generation completed.")

@cli.command()
@click.option("--path", "-p", type=click.Path(exists=True), multiple=True, help="Path(s) to analyze.")
@click.option("--format", type=click.Choice(["flat", "tree"]), default="flat", help="Format of the analysis output.")
@click.pass_context
def analyze(ctx, **options):
    """Analyze codebase structure
    This command analyzes the structure of the specified codebase and provides an output in either a flat or tree-like format, summarizing the files and their relationships.
    Args:
        ctx: The Click context object.
        options: Various options for customizing the analysis output.
    """
    config = ctx.obj["config"].merge(options)
    logger = setup_logger(level=config.log_level)
    logger.info("Analyzing codebase with options: %s", options)

    command = AnalyzeCommand(config, logger)
    command.execute()

    logger.info("Codebase analysis completed.")

def get_directory_tree(path):
    """Retrieve a list of files and directories in a given path."""
    return [p.name for p in Path(path).iterdir() if p.is_file() or p.is_dir()]

def format_tree(tree, indent=''):
    """Format the directory tree for display."""
    lines = []
    for i, line in enumerate(tree):
        lines.append(f"{indent}{line}")
    return lines

@cli.command()
@click.option("--path", "-p", type=click.Path(exists=True), default=".", help="Path to the directory to select files from.")
@click.pass_context
def interactive(ctx, path):
    """Interactive file selection"""
    tree = get_directory_tree(path)
    selected_files = []
    cursor_position = 0

    kb = KeyBindings()

    @kb.add('q')
    def _(event):
        event.app.exit()

    @kb.add('up')
    def _(event):
        nonlocal cursor_position
        cursor_position = max(0, cursor_position - 1)

    @kb.add('down')
    def _(event):
        nonlocal cursor_position
        cursor_position = min(len(tree) - 1, cursor_position + 1)

    @kb.add('space')
    def _(event):
        toggle_selection()

    @kb.add('enter')
    def _(event):
        event.app.exit()

    def toggle_selection():
        nonlocal selected_files
        current_item = tree[cursor_position]
        full_path = str(Path(path) / current_item)
        if full_path in selected_files:
            selected_files.remove(full_path)
        else:
            selected_files.append(full_path)

    def get_formatted_text():
        result = []
        for i, line in enumerate(tree):
            style = 'class:cursor' if i == cursor_position else ''
            checkbox = '[X]' if str(Path(path) / line) in selected_files else '[ ]'
            result.append((style, f"{checkbox} {line}\n"))
        return result

    # Create a scrollable window
    tree_window = Window(
        content=FormattedTextControl(get_formatted_text),
        width=60,
        dont_extend_width=True,
        wrap_lines=False,
        focusable=True,
    )

    instructions = HTML('Use arrow keys to navigate, space to select, enter to confirm, q to quit')
    layout = Layout(HSplit([tree_window, Window(content=FormattedTextControl(instructions))]))

    app = Application(layout=layout, key_bindings=kb, full_screen=True)
    app.run()

    if selected_files:
        logging.info("Selected files: %s", selected_files)
        ctx.invoke(generate, path=selected_files)
    else:
        logging.info("No files selected.")

if __name__ == "__main__":
    cli(standalone_mode=False)