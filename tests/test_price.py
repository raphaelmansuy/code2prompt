import pytest
from code2prompt.utils.price_calculator import TokenPrices, PriceModel, Provider, calculate_prices, PriceResult

@pytest.fixture
def sample_token_prices():
    return TokenPrices(
        providers=[
            Provider(
                name="OpenAI",
                models=[
                    PriceModel(name="GPT-3", price=0.02),
                    PriceModel(name="GPT-4", input_price=0.03, output_price=0.06),
                ]
            ),
            Provider(
                name="Anthropic",
                models=[
                    PriceModel(name="Claude", input_price=0.01, output_price=0.03),
                ]
            )
        ]
    )

def test_calculate_prices_all_providers_and_models(sample_token_prices):
    results = calculate_prices(sample_token_prices, 1000, 500)
    assert len(results) == 3
    assert {r.provider_name for r in results} == {"OpenAI", "Anthropic"}
    assert {r.model_name for r in results} == {"GPT-3", "GPT-4", "Claude"}

def test_calculate_prices_specific_provider(sample_token_prices):
    results = calculate_prices(sample_token_prices, 1000, 500, provider="OpenAI")
    assert len(results) == 2
    assert all(r.provider_name == "OpenAI" for r in results)

def test_calculate_prices_specific_model(sample_token_prices):
    results = calculate_prices(sample_token_prices, 1000, 500, model="GPT-4")
    assert len(results) == 1
    assert results[0].model_name == "GPT-4"

def test_calculate_prices_non_existent_provider(sample_token_prices):
    results = calculate_prices(sample_token_prices, 1000, 500, provider="NonExistent")
    assert len(results) == 0

def test_calculate_prices_non_existent_model(sample_token_prices):
    results = calculate_prices(sample_token_prices, 1000, 500, model="NonExistent")
    assert len(results) == 0

def test_calculate_prices_single_price_model(sample_token_prices):
    results = calculate_prices(sample_token_prices, 1000, 500, model="GPT-3")
    assert len(results) == 1
    result = results[0]
    assert result.price_input == 0.02
    assert result.price_output == 0.02
    assert result.total_price == pytest.approx(0.03)  # (1000 + 500) * 0.02 / 1000

def test_calculate_prices_separate_input_output_prices(sample_token_prices):
    results = calculate_prices(sample_token_prices, 1000, 500, model="GPT-4")
    assert len(results) == 1
    result = results[0]
    assert result.price_input == 0.03
    assert result.price_output == 0.06
    assert result.total_price == pytest.approx(0.06)  # (1000 * 0.03 + 500 * 0.06) / 1000

def test_calculate_prices_zero_tokens(sample_token_prices):
    results = calculate_prices(sample_token_prices, 0, 0)
    assert len(results) == 3
    assert all(r.total_price == 0 for r in results)



def test_calculate_prices_result_structure(sample_token_prices):
    results = calculate_prices(sample_token_prices, 1000, 500, model="GPT-4")
    assert len(results) == 1
    result = results[0]
    assert isinstance(result, PriceResult)
    assert hasattr(result, 'provider_name')
    assert hasattr(result, 'model_name')
    assert hasattr(result, 'price_input')
    assert hasattr(result, 'price_output')
    assert hasattr(result, 'total_tokens')
    assert hasattr(result, 'total_price')

def test_calculate_prices_total_tokens(sample_token_prices):
    results = calculate_prices(sample_token_prices, 1000, 500)
    assert all(r.total_tokens == 1500 for r in results)

@pytest.mark.parametrize("input_tokens,output_tokens,expected_total", [
    (1000, 500, 1500),
    (0, 1000, 1000),
    (1000, 0, 1000),
    (0, 0, 0),
])
def test_calculate_prices_various_token_combinations(sample_token_prices, input_tokens, output_tokens, expected_total):
    results = calculate_prices(sample_token_prices, input_tokens, output_tokens)
    assert all(r.total_tokens == expected_total for r in results)



def test_calculate_prices_empty_token_prices():
    empty_token_prices = TokenPrices(providers=[])
    results = calculate_prices(empty_token_prices, 1000, 500)
    assert len(results) == 0
