from code2prompt.version import VERSION


import click


def print_help(_ctx):
    """Print comprehensive help information."""
    click.echo(click.style("code2prompt CLI Tool", fg="green", bold=True))
    click.echo(f"Version: {VERSION}\n")

    click.echo(click.style("Description:", fg="yellow", bold=True))
    click.echo("code2prompt is a powerful CLI tool for generating markdown documentation from code files and analyzing codebase structure.\n")

    click.echo(click.style("Usage:", fg="yellow", bold=True))
    click.echo("  code2prompt [OPTIONS] COMMAND [ARGS]...\n")

    click.echo(click.style("Commands:", fg="yellow", bold=True))
    click.echo("  generate    Generate markdown from code files")
    click.echo("  analyze     Analyze codebase structure\n")

    click.echo(click.style("Global Options:", fg="yellow", bold=True))
    click.echo("  --config PATH                 Path to configuration file")
    click.echo("  -v, --version                 Show the version and exit")
    click.echo("  --help                        Show this message and exit\n")

    click.echo(click.style("Generate Command Options:", fg="yellow", bold=True))
    click.echo("  -p, --path PATH               Path(s) to the directory or file to process")
    click.echo("  -o, --output PATH             Name of the output Markdown file")
    click.echo("  -g, --gitignore PATH          Path to the .gitignore file")
    click.echo("  -f, --filter TEXT             Comma-separated filter patterns to include files")
    click.echo("  -e, --exclude TEXT            Comma-separated patterns to exclude files")
    click.echo("  --case-sensitive              Perform case-sensitive pattern matching")
    click.echo("  -s, --suppress-comments       Strip comments from the code files")
    click.echo("  -ln, --line-number            Add line numbers to source code blocks")
    click.echo("  --no-codeblock                Disable wrapping code inside markdown code blocks")
    click.echo("  -t, --template PATH           Path to a Jinja2 template file for custom prompt generation")
    click.echo("  --tokens                      Display the token count of the generated prompt")
    click.echo("  --encoding [cl100k_base|p50k_base|p50k_edit|r50k_base]")
    click.echo("                                Specify the tokenizer encoding to use")
    click.echo("  --create-templates            Create a templates directory with example templates")
    click.echo("  --log-level [DEBUG|INFO|WARNING|ERROR|CRITICAL]")
    click.echo("                                Set the logging level")
    click.echo("  --price                       Display the estimated price of tokens")
    click.echo("  --provider TEXT               Specify the provider for price calculation")
    click.echo("  --model TEXT                  Specify the model for price calculation")
    click.echo("  --output-tokens INTEGER       Specify the number of output tokens for price calculation\n")

    click.echo(click.style("Analyze Command Options:", fg="yellow", bold=True))
    click.echo("  -p, --path PATH               Path(s) to analyze")
    click.echo("  --format [flat|tree]          Format of the analysis output\n")

    click.echo(click.style("Examples:", fg="yellow", bold=True))
    click.echo("  code2prompt generate -p ./src")
    click.echo("  code2prompt analyze -p ./src --format tree")
    click.echo("  code2prompt generate -p ./src -o output.md --price --provider openai --model gpt-3.5-turbo\n")

    click.echo(click.style("Note:", fg="red", bold=True))
    click.echo("🚨 code2prompt 0.7.0 is a major version update from code2doc.")
    click.echo("🤖 Starting with version 0.7.0, you must use 'code2prompt generate' to generate content from code files.")
    click.echo()
    click.echo(click.style("For more information, visit:", fg="cyan"))
    click.echo("https://github.com/raphaelmansuy/code2prompt")
    click.echo()
    click.echo("Created with ❤️ by Raphael Mansuy")
    
    