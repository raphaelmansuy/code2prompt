import click
import tiktoken


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