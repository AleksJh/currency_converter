import pytest
from currency_app.main import get_exchange_rates

def test_get_exchange_rates_success(mocker):
    fake_response = {
        "success": True,
        "quotes": {
            "USDGBP": 0.75,
            "USDEUR": 0.9
        }
    }

    mock_get = mocker.patch("currency_app.main.requests.get")
    mock_get.return_value.json.return_value = fake_response

    api_key = "apitest"
    currencies = ["EUR", "GBP"]
    rates = get_exchange_rates(api_key, currencies)

    assert rates["USDGBP"] == 0.75
    assert rates["USDEUR"] == 0.9


