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

def calculate_prices(token_prices, input_tokens, output_tokens, provider=None, model=None):
    """
    Calculate the prices for a given number of input and output tokens based on token prices.

    Args:
        token_prices (dict): A dictionary containing token prices for different providers and models.
        input_tokens (int): The number of input tokens.
        output_tokens (int): The number of output tokens.
        provider (str, optional): The name of the provider. If specified, only prices for the specified provider will be calculated. Defaults to None.
        model (str, optional): The name of the model. If specified, only prices for the specified model will be calculated. Defaults to None.

    Returns:
        list: A list of tuples containing the provider name, model name, price per token, total tokens, and total price for each calculation.

    """
def calculate_prices(token_prices, input_tokens, output_tokens, provider=None, model=None):
    results = []
    
    for p in token_prices["providers"]:
        if provider and p["name"] != provider:
            continue
        
        for m in p["models"]:
            if model and m["name"] != model:
                continue
            
            total_tokens = input_tokens + output_tokens
            
            if "price" in m:
                # Single price for both input and output tokens
                price = m["price"]
                total_price = (price * total_tokens) / 1000
                price_info = f"${price:.10f}"
            elif "input_price" in m and "output_price" in m:
                # Separate prices for input and output tokens
                input_price = m["input_price"]
                output_price = m["output_price"]
                total_price = ((input_price * input_tokens) + (output_price * output_tokens)) / 1000
                price_info = f"${input_price:.10f} (input) / ${output_price:.10f} (output)"
            else:
                # Skip models with unexpected price structure
                continue
            
            result = (
                p["name"],                  # Provider name
                m["name"],                  # Model name
                price_info,                 # Price information
                total_tokens,               # Total number of tokens
                f"${total_price:.10f}"      # Total price
            )
            
            results.append(result)
    
    return results