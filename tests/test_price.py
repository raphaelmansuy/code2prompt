import pytest
from pathlib import Path
from unittest.mock import patch, mock_open
from code2prompt.utils.price_calculator import load_token_prices, calculate_prices
from code2prompt.main import create_markdown_file

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

def test_calculate_prices_specific_provider_model(mock_token_prices):
    result = calculate_prices(mock_token_prices, 1000, 1000, "provider1", "model1")
    assert len(result) == 1
    assert result[0][0] == "provider1"
    assert result[0][1] == "model1"
    assert result[0][2] == "$0.100000"
    assert result[0][3] == 1000
    assert result[0][4] == "$0.20"

def test_calculate_prices_all_providers_models(mock_token_prices):
    result = calculate_prices(mock_token_prices, 1000, 1000)
    assert len(result) == 4

def test_calculate_prices_specific_provider(mock_token_prices):
    result = calculate_prices(mock_token_prices, 1000, 1000, "provider1")
    assert len(result) == 2
    assert all(row[0] == "provider1" for row in result)

def test_calculate_prices_zero_tokens(mock_token_prices):
    result = calculate_prices(mock_token_prices, 0, 0)
    assert all(row[4] == "$0.00" for row in result)



