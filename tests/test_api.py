from currency_app.main import get_exchange_rates
from pathlib import Path


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

    mock_cache_file = mocker.Mock(spec=Path)
    # Make '.exist'=False, so that it calls API
    mock_cache_file.exists.return_value = False
    # Mocking the file, to prevent writing in the real one
    mock_open = mocker.patch('builtins.open', mocker.mock_open())
    rates = get_exchange_rates(api_key, mock_cache_file)

    assert rates["USDGBP"] == 0.75
    assert rates["USDEUR"] == 0.9

    mock_open.assert_called_with(mock_cache_file, "w", encoding="utf-8")
