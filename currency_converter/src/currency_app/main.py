from dotenv import load_dotenv
import os
import sys
import requests

VALID_CURRENCY_CODES = {
    "USD", "EUR", "GBP", "JPY", "CAD", "AUD", "CHF", "CNY", "RUB", "INR", "BRL", "TRY"
}

API_URL = "https://api.currencylayer.com/live"

def load_api_key():
    load_dotenv()
    key = os.getenv("CURRENCYLAYER_API_KEY")
    if not key:
        print('API key not found. Please set it in a .env file.')
        sys.exit(1)
    return key


def get_exchange_rates(api_key, currencies):
    params = {
        "access_key": api_key,
        "currencies": ','.join(currencies),
        "format": 1
    }

    try:
        response = requests.get(API_URL, params=params, timeout=10)
        data = response.json()
        if not data.get("success", False):
            raise ValueError(data.get("error", {}).get("info", "Unknown error"))
        return data["quotes"]
    except Exception as e:
        print(f'Failed to get exchange rates: {e}')
        sys.exit(1)


def validate_currency(code):
    return code.upper() in VALID_CURRENCY_CODES


def convert(from_cur, to_cur, amount, rates):
    if from_cur == "USD":
        usd_amount = amount
    else:
        # We are on the free plan which means only USD is supported as the base currency.
        # So to convert x to y, we need to covert x->USD, then USD->y.
        rate = rates.get("USD"+from_cur)
        if not rate:
            raise ValueError(f"No rate for USD -> {from_cur}")
        usd_amount = amount / rate

    to_rate = rates.get("USD"+to_cur)
    if not to_rate:
        raise ValueError(f"No rate for USD -> {to_cur}")

    return round(usd_amount * to_rate, 2)


def main():
    print("Aleksan's Currency Converter (using data from currencylayer.com)\n")

    from_cur = input('From currency (e.g. EUR): ').upper()
    to_cur = input('To currency (e.g. GBP): ').upper()
    try:
        amount = float(input('Amount: '))
    except ValueError:
        print('Invalid amount. Must be a number.')
        return

    if not (validate_currency(from_cur) and validate_currency(to_cur)):
        print('Invalid currency code.')
        return

    api_key = load_api_key()
    needed_currencies = {from_cur, to_cur}
    if "USD" not in needed_currencies:
        needed_currencies.add("USD")

    rates = get_exchange_rates(api_key, needed_currencies)
    result = convert(from_cur, to_cur, rates)

    print(f'\n{amount} {from_cur} = {result} {to_cur}')


if __name__ == "__main__":
    main()





