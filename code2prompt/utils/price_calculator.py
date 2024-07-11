import json
from pathlib import Path

def load_token_prices():
    """
    Load token prices from a JSON file.

    Returns:
        dict: A dictionary containing token prices.

    Raises:
        RuntimeError: If there is an error loading the token prices.
    """
    price_file = Path(__file__).parent.parent / "data" / "token_price.json"
    try:
        with open(price_file, "r", encoding="utf-8") as f:
            return json.load(f)
    except (IOError, json.JSONDecodeError) as e:
        raise RuntimeError(f"Error loading token prices: {str(e)}") from e

def calculate_price(token_count, price_per_1000):
    """
    Calculates the price based on the token count and price per 1000 tokens.

    Args:
        token_count (int): The total number of tokens.
        price_per_1000 (float): The price per 1000 tokens.

    Returns:
        float: The calculated price.
    """
    return (token_count / 1_000) * price_per_1000

def calculate_prices(token_prices, input_token_count, output_token_count, provider=None, model=None):
    """
    Calculate the prices based on the token prices, input and output token counts, provider, and model.

    Args:
        token_prices (dict): A dictionary containing token prices for different providers and models.
        input_token_count (int): The number of input tokens.
        output_token_count (int): The number of output tokens.
        provider (str, optional): The name of the provider. If specified, only prices for this provider will be calculated. Defaults to None.
        model (str, optional): The name of the model. If specified, only prices for this model will be calculated. Defaults to None.

    Returns:
        list: A list of lists containing the calculated prices for each provider and model. Each inner list contains the following information:
            - Provider name
            - Model name
            - Input price
            - Input token count
            - Total price
    """
    table_data = []
    for provider_data in token_prices["providers"]:
        # Convert both strings to lowercase for case-insensitive comparison
        if provider and provider_data["name"].lower() != provider.lower():
            continue
        for model_data in provider_data["models"]:
            # Convert both strings to lowercase for case-insensitive comparison
            if model and model_data["name"].lower() != model.lower():
                continue
            
            input_price = model_data.get("input_price", model_data.get("price", 0))
            output_price = model_data.get("output_price", model_data.get("price", 0))
            
            total_price = (
                calculate_price(input_token_count, input_price) +
                calculate_price(output_token_count, output_price)
            )
            
            table_data.append([
                provider_data["name"],
                model_data["name"],
                f"${input_price:.6f}",
                input_token_count,
                f"${total_price:.2f}"
            ])
    
    return table_data