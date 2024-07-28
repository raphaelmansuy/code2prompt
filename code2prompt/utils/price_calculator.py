import json
from typing import List, Optional
from pathlib import Path
from functools import lru_cache
from pydantic import BaseModel, ConfigDict, field_validator


class PriceModel(BaseModel):
    price: Optional[float] = None
    input_price: Optional[float] = None
    output_price: Optional[float] = None
    name: str

    @field_validator("price", "input_price", "output_price")
    @classmethod
    def check_price(cls, v: Optional[float]) -> Optional[float]:
        if v is not None and v < 0:
            raise ValueError("Price must be non-negative")
        return v


class Provider(BaseModel):
    name: str
    models: List[PriceModel]


class TokenPrices(BaseModel):
    providers: List[Provider]


class PriceResult(BaseModel):
    provider_name: str
    model_name: str
    price_input: float
    price_output: float
    total_tokens: int
    total_price: float
    
    model_config = ConfigDict(protected_namespaces=())




@lru_cache(maxsize=1)
def load_token_prices() -> TokenPrices:
    """
    Load token prices from a JSON file.

    Returns:
        TokenPrices: A Pydantic model containing token prices.

    Raises:
        RuntimeError: If there is an error loading the token prices.
    """
    price_file = Path(__file__).parent.parent / "data" / "token_price.json"
    try:
        with price_file.open("r", encoding="utf-8") as f:
            data = json.load(f)
            return TokenPrices.model_validate(data)
    except (IOError, json.JSONDecodeError) as e:
        raise RuntimeError(f"Error loading token prices: {str(e)}") from e


def calculate_price(token_count: int, price_per_1000: float) -> float:
    """
    Calculates the price based on the token count and price per 1000 tokens.

    Args:
        token_count (int): The total number of tokens.
        price_per_1000 (float): The price per 1000 tokens.

    Returns:
        float: The calculated price.
    """
    return (token_count / 1_000) * price_per_1000


def calculate_prices(
    token_prices: TokenPrices,
    input_tokens: int,
    output_tokens: int,
    provider: Optional[str] = None,
    model: Optional[str] = None,
) -> List[PriceResult]:
    """
    Calculate the prices for a given number of input and output tokens based on token prices.

    Args:
        token_prices (TokenPrices): A Pydantic model containing token prices for different providers and models.
        input_tokens (int): The number of input tokens.
        output_tokens (int): The number of output tokens.
        provider (str, optional): The name of the provider. If specified, only prices for the specified provider will be calculated.
        model (str, optional): The name of the model. If specified, only prices for the specified model will be calculated.

    Returns:
        List[PriceResult]: A list of PriceResult objects containing the calculation results.
    """
    results = []
    total_tokens = input_tokens + output_tokens

    for provider_data in token_prices.providers:
        if provider and provider_data.name.lower() != provider.lower():
            continue

        for model_data in provider_data.models:
            if model and model_data.name.lower() != model.lower():
                continue

            if model_data.price is not None:
                price_input = model_data.price
                price_output = model_data.price
                total_price = calculate_price(total_tokens, model_data.price)
            elif (
                model_data.input_price is not None
                and model_data.output_price is not None
            ):
                price_input = model_data.input_price
                price_output = model_data.output_price
                total_price = calculate_price(
                    input_tokens, price_input
                ) + calculate_price(output_tokens, price_output)
            else:
                continue

            results.append(
                PriceResult(
                    provider_name=provider_data.name,
                    model_name=model_data.name,
                    price_input=price_input,
                    price_output=price_output,
                    total_tokens=total_tokens,
                    total_price=total_price,
                )
            )

    return results


if __name__ == "__main__":
    # Example usage
    token_prices = load_token_prices()
    results = calculate_prices(token_prices, input_tokens=100, output_tokens=50)
    for result in results:
        print(f"Provider: {result.provider_name}")
        print(f"Model: {result.model_name}")
        print(f"Input Price: ${result.price_input:.10f}")
        print(f"Output Price: ${result.price_output:.10f}")
        print(f"Total Tokens: {result.total_tokens}")
        print(f"Total Price: ${result.total_price:.10f}")
        print("---")