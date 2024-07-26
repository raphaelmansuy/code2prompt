import pytest
from unittest.mock import patch, mock_open
from code2prompt.utils.price_calculator import load_token_prices, calculate_prices

# Mock JSON data
MOCK_JSON_DATA = '''
{
    "providers": [
        {
            "name": "provider1",
            "models": [
                {
                    "name": "model1",
                    "price": 0.1
                },
                {
                    "name": "model2",
                    "input_price": 0.3,
                    "output_price": 0.4
                }
            ]
        },
        {
            "name": "provider2",
            "models": [
                {
                    "name": "model1",
                    "input_price": 0.3,
                    "output_price": 0.4
                },
                {
                    "name": "model2",
                    "input_price": 0.3,
                    "output_price": 0.4
                }
            ]
        }
    ]
}
'''

@pytest.fixture
def mock_token_prices():
    with patch("builtins.open", mock_open(read_data=MOCK_JSON_DATA)):
        yield load_token_prices()

def test_load_token_prices_success(mock_token_prices):
    assert len(mock_token_prices["providers"]) == 2
    assert mock_token_prices["providers"][0]["name"] == "provider1"
    assert mock_token_prices["providers"][1]["name"] == "provider2"

def test_load_token_prices_file_not_found():
    with patch("builtins.open", side_effect=FileNotFoundError):
        with pytest.raises(RuntimeError, match="Error loading token prices"):
            load_token_prices()

def test_load_token_prices_invalid_json():
    with patch("builtins.open", mock_open(read_data="invalid json")):
        with pytest.raises(RuntimeError, match="Error loading token prices"):
            load_token_prices()

def test_calculate_prices_single_price_model(mock_token_prices):
    result = calculate_prices(mock_token_prices, 1000, 1000, "provider1", "model1")
    assert len(result) == 1
    assert result[0] == ("provider1", "model1", "$0.1000000000", 2000, "$0.2000000000")

def test_calculate_prices_dual_price_model(mock_token_prices):
    result = calculate_prices(mock_token_prices, 1000, 2000, "provider1", "model2")
    assert len(result) == 1
    assert result[0] == ("provider1", "model2", "$0.3000000000 (input) / $0.4000000000 (output)", 3000, "$1.1000000000")

def test_calculate_prices_all_providers_models(mock_token_prices):
    result = calculate_prices(mock_token_prices, 1000, 1000)
    assert len(result) == 4
    assert set(row[0] for row in result) == {"provider1", "provider2"}
    assert set(row[1] for row in result) == {"model1", "model2"}

def test_calculate_prices_specific_provider(mock_token_prices):
    result = calculate_prices(mock_token_prices, 1000, 1000, "provider1")
    assert len(result) == 2
    assert all(row[0] == "provider1" for row in result)
    assert set(row[1] for row in result) == {"model1", "model2"}

def test_calculate_prices_zero_tokens(mock_token_prices):
    result = calculate_prices(mock_token_prices, 0, 0)
    assert len(result) == 4
    assert all(row[4] == "$0.0000000000" for row in result)

def test_calculate_prices_different_input_output_tokens(mock_token_prices):
    result = calculate_prices(mock_token_prices, 1000, 2000, "provider2", "model1")
    assert len(result) == 1
    assert result[0] == ("provider2", "model1", "$0.3000000000 (input) / $0.4000000000 (output)", 3000, "$1.1000000000")

def test_calculate_prices_non_existent_provider(mock_token_prices):
    result = calculate_prices(mock_token_prices, 1000, 1000, "non_existent_provider")
    assert len(result) == 0

def test_calculate_prices_non_existent_model(mock_token_prices):
    result = calculate_prices(mock_token_prices, 1000, 1000, "provider1", "non_existent_model")
    assert len(result) == 0

def test_calculate_prices_large_numbers(mock_token_prices):
    result = calculate_prices(mock_token_prices, 1000000, 1000000, "provider1", "model1")
    assert len(result) == 1
    assert result[0] == ("provider1", "model1", "$0.1000000000", 2000000, "$200.0000000000")

def test_calculate_prices_small_numbers(mock_token_prices):
    result = calculate_prices(mock_token_prices, 1, 1, "provider1", "model1")
    assert len(result) == 1
    assert result[0] == ("provider1", "model1", "$0.1000000000", 2, "$0.0002000000")

def test_calculate_prices_floating_point_precision(mock_token_prices):
    result = calculate_prices(mock_token_prices, 1000, 1000, "provider2", "model1")
    assert len(result) == 1
    assert result[0] == ("provider2", "model1", "$0.3000000000 (input) / $0.4000000000 (output)", 2000, "$0.7000000000")