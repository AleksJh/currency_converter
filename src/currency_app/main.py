from dotenv import load_dotenv
import logging
import os
import sys
import requests

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("currency_converter.log"),
        logging.StreamHandler()
    ]
)

VALID_CURRENCY_CODES = set()

API_URL = "https://api.currencylayer.com/live"


def valid_currency_codes_update():
    from secondary import parse_currency_codes_from_html
    new_codes = parse_currency_codes_from_html('cl-currencies-table.txt')
    VALID_CURRENCY_CODES.update(new_codes)
    logging.debug(f"Function finished. Added {len(new_codes)} new codes.")


def load_api_key():
    logging.debug("Attempting to load API key from .env")
    # python-dotenv reads key-value pairs from a .env file and can set
    # them as environment variables.
    load_dotenv()
    key = os.getenv("CURRENCYLAYER_API_KEY")
    if not key:
        logging.error("API key not found. Exiting.")
        print('API key not found. Please set it in a .env file.')
        sys.exit(1)
    logging.info("API key loaded successfully")
    return key


def get_exchange_rates(api_key, currencies):
    logging.info(f"Getting rates for: {currencies}")
    params = {
        "access_key": api_key,
        "currencies": ','.join(currencies),
        "format": 1
    }

    try:
        logging.info(f"Requesting exchange rates for: {currencies}")
        response = requests.get(API_URL, params=params, timeout=10)
        data = response.json()
        if not data.get("success", False):
            error_info = data.get("error", {}).get("info", "Unknown error")
            logging.error(f"API returned error: {error_info}")
            raise ValueError(error_info)
        logging.info("Exchange rates received successfully.")
        return data["quotes"]
    except Exception as e:
        logging.exception("Failed while fetching exchange rates")
        print(f'Failed to get exchange rates: {e}')
        sys.exit(1)


def validate_currency(code):
    logging.debug(f"Validating currency: {code}")
    return code.upper() in VALID_CURRENCY_CODES


def convert(from_cur, to_cur, amount, rates):
    logging.debug(f"Converting {amount} {from_cur} {to_cur}")
    if from_cur == to_cur:
        logging.info("Same currency, returning successfully")
        return round(amount, 2)

    if from_cur == "USD":
        logging.info('from_cur == "USD":')
        to_rate = rates.get("USD"+to_cur)
        if not to_rate:
            logging.exception(f'No rate for USD -> {to_cur}')
            raise ValueError(f'No rate for USD -> {to_cur}')
        logging.info(f'Converted from USD to {to_cur} successfully')
        return round(amount*to_rate, 2)

    if to_cur == "USD":
        logging.info('to_cur == "USD"')
        from_rate = rates.get("USD"+from_cur)
        if not from_rate:
            logging.exception(f"No rate for USD -> {from_rate}")
            raise ValueError(f"No rate for USD -> {from_rate}")
        logging.info(f'Converted from {from_cur} to USD successfully')
        return round(amount / from_rate, 2)

    # other -> other
    # x -> y : x->USD, then USD->y
    logging.info("Other to other (not USD)")
    from_rate = rates.get("USD"+from_cur)
    to_rate = rates.get("USD"+to_cur)
    if not from_rate:
        logging.exception(f'No rate for USD -> {from_cur}')
        raise ValueError(f"No rate for USD -> {from_cur}")
    if not to_rate:
        logging.exception(f'No rate for USD -> {to_cur}')
        raise ValueError(f"No rate for USD -> {to_cur}")

    usd_amount = amount / from_rate
    logging.info(f"Converted {from_cur} to {to_cur} successfully")
    return round(usd_amount * to_rate, 2)


def main():
    logging.info("Started currency converter")
    print("Aleksan's Currency Converter (using data from currencylayer.com)\n")

    logging.info('Updating available currencies set')
    valid_currency_codes_update()
    print('The set of currencies updated')

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
    # x -> y : x->USD, then USD->y.
    if "USD" not in needed_currencies:
        needed_currencies.add("USD")

    rates = get_exchange_rates(api_key, needed_currencies)
    result = convert(from_cur, to_cur, amount, rates)

    print(f'\n{amount} {from_cur} = {result} {to_cur}')


if __name__ == "__main__":
    main()


# TODO: Add historic data

# TODO: Github doesn't pull up the .env file. We need to come up with a script
#  for this situation, with a check for the presence
#  and a suggestion to enter the API key there.
