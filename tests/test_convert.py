from currency_app.main import convert


def test_convert_other_to_other():
    rates = {"USDEUR": 0.9, "USDGBP": 0.75}
    result = convert("EUR", "GBP", 100, rates)
    # EUR/USD: 100/0.9 = 111.11, then * 0.75 = 83.33
    assert round(result, 2) == 83.33


def test_convert_usd_to_other():
    rates = {"USDGBP": 0.75}
    result = convert("USD", "GBP", 100, rates)
    assert result == 75.0


def test_convert_to_usd():
    rates = {"USDEUR": 0.9}
    result = convert("EUR", "USD", 90, rates)
    assert result == 100.0


# Parametrized version is possible with this decorator
# @pytest.mark.parametrize(
#     "from_cur, to_cur, amount, expected_result, rates",
#     [
#         ("EUR", "GBP", 100, 83.33, {"USDEUR": 0.9, "USDGBP": 0.75}), # other
#                                                                      to other
#         ("USD", "GBP", 100, 75.0, {"USDGBP": 0.75}),           # USD to other
#         ("EUR", "USD", 90, 100.0, {"USDEUR": 0.9}),            # to USD
#         ("USD", "USD", 50, 50.0, {}),                          # Same
#                                                                # currency
