from code2prompt.utils.price_calculator import calculate_prices, load_token_prices

import click
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text


def format_price(price: float, is_total: bool = False) -> str:
    """
    Formats the given price as a string.

    Args:
        price (float): The price to be formatted.
        is_total (bool, optional): Indicates whether the price is a total. Defaults to False.

    Returns:
        str: The formatted price as a string.

    """
    if is_total:
        return f"${price:.6f}"
    return f"${price /1_000 * 1_000_000 :.2f}"


def format_specific_price(price: float, tokens: int) -> str:
    """
    Formats the specific price based on the given price and tokens.

    Args:
        price (float): The price value.
        tokens (int): The number of tokens.

    Returns:
        str: The formatted specific price.

    """
    return f"${(price * tokens / 1_000):.6f}"


def display_price_table(
    output_tokens: int, provider: str, model: str, token_count: int
):
    """
    Displays a price table with estimated token prices based on the token count and provider's pricing model.

    Args:
        output_tokens (int): The number of output tokens.
        provider (str): The name of the provider.
        model (str): The name of the model.
        token_count (int): The number of input tokens.

    Returns:
        None
    """
    token_prices = load_token_prices()
    if not token_prices:
        return
    price_results = calculate_prices(
        token_prices, token_count, output_tokens, provider, model
    )

    if not price_results:
        click.echo("Error: No matching provider or model found")
        return

    console = Console()

    table = Table(show_header=True, header_style="bold magenta", expand=True)
    table.add_column("Provider", style="cyan", no_wrap=True)
    table.add_column("Model", style="green")
    table.add_column("Input Price\n($/1M tokens)", justify="right", style="yellow")
    table.add_column("Output Price\n($/1M tokens)", justify="right", style="yellow")
    table.add_column("Tokens\nOut | In", justify="right", style="blue")
    table.add_column("Price $\nOut | In", justify="right", style="magenta")
    table.add_column("Total Cost", justify="right", style="red")

    for result in price_results:
        input_price = format_price(result.price_input)
        output_price = format_price(result.price_output)
        specific_input_price = format_specific_price(result.price_input, token_count)
        specific_output_price = format_specific_price(
            result.price_output, output_tokens
        )
        total_price = format_price(result.total_price, is_total=True)

        table.add_row(
            result.provider_name,
            result.model_name,
            input_price,
            output_price,
            f"{token_count:,} | {output_tokens:,}",
            f"{specific_input_price} | {specific_output_price}",
            total_price,
        )

    title = Text("Estimated Token Prices", style="bold white on blue")
    subtitle = Text("All prices in USD", style="italic")

    panel = Panel(
        table, title=title, subtitle=subtitle, expand=False, border_style="blue"
    )

    console.print("\n")
    console.print(panel)
    console.print(
        "\n📊 Note: Prices are based on the token count and provider's pricing model."
    )
    console.print(
        "💡 Tip: 'Price $ In | Out' shows the cost for the specific input and output tokens."
    )
    console.print(
        "⚠️  This is an estimate based on OpenAI's Tokenizer implementation.\n"
    )
