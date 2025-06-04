import os
import sys
import requests
import logging
import json
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv
from currency_app.secondary import parse_currency_codes_from_json

CACHE_FILE = Path(__file__).parent / "exchange_rates_cache.json"

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
    new_codes = parse_currency_codes_from_json('cl-currencies.json')
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


def get_exchange_rates(api_key: str, cache_file: Path) -> dict:
    """
    Returns a dictionary of exchange rates (quotes) from currencylayer.com.
    Uses a local JSON cache file to avoid unnecessary API requests.

    Workflow:
    - If the cache file exists and was created today, use its data
    - Otherwise, fetch new data from the API, cache it, and return it

    Args:
        api_key (str): Currencylayer API key
        cache_file (Path): Path to the local JSON cache file

    Returns:
        dict: Dictionary of exchange rate quotes, e.g., {"USDEUR": 0.91, "USDJPY": 143.2}
    """

    def is_today(timestamp_str: str) -> bool:
        """Returns True if the ISO timestamp is from today."""
        try:
            ts = datetime.fromisoformat(timestamp_str)
            return ts.date() == datetime.now().date()
        except Exception:
            return False

    if cache_file.exists():
        try:
            with open(cache_file, "r", encoding="utf-8") as f:
                cache_data = json.load(f)
            if "timestamp" in cache_data and is_today(cache_data["timestamp"]):
                logging.info("Using cached exchange rates")
                return cache_data["quotes"]
            else:
                logging.info("Cache is outdated, will refresh")
        except Exception as e:
            logging.warning(f"Failed to load cache: {e}")

    # Fetch fresh data from the API
    params = {
        "access_key": api_key,
        "format": 1
    }

    try:
        response = requests.get("https://api.currencylayer.com/live", params=params, timeout=10)
        data = response.json()

        if not data.get("success", False):
            raise ValueError(data.get("error", {}).get("info", "Unknown error"))

        quotes = data["quotes"]

        # Save to cache with timestamp
        with open(cache_file, "w", encoding="utf-8") as f:
            json.dump({
                "timestamp": datetime.now().isoformat(),
                "quotes": quotes
            }, f)

        logging.info("Cached new exchange rates")
        return quotes

    except Exception as e:
        logging.critical(f"Could not fetch or cache exchange rates: {e}")
        raise


def validate_currency(code):
    logging.debug(f"Validating currency: {code}")
    return code.upper() in VALID_CURRENCY_CODES


def convert(from_cur, to_cur, amount, rates):
    logging.debug(f"Converting {amount} {from_cur} {to_cur}")
    if from_cur == to_cur:
        logging.debug("Same currency, returning successfully")
        return round(amount, 2)

    if from_cur == "USD":
        logging.debug('from_cur == "USD":')
        to_rate = rates.get("USD"+to_cur)
        if not to_rate:
            logging.exception(f'No rate for USD -> {to_cur}')
            raise ValueError(f'No rate for USD -> {to_cur}')
        logging.info(f'Converted from USD to {to_cur} successfully')
        return round(amount*to_rate, 2)

    if to_cur == "USD":
        logging.debug('to_cur == "USD"')
        from_rate = rates.get("USD"+from_cur)
        if not from_rate:
            logging.exception(f"No rate for USD -> {from_rate}")
            raise ValueError(f"No rate for USD -> {from_rate}")
        logging.info(f'Converted from {from_cur} to USD successfully')
        return round(amount / from_rate, 2)

    # other -> other
    # x -> y : x->USD, then USD->y
    logging.debug("Other to other (not USD)")
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
    logging.debug("Started currency converter")
    print("Aleksan's Currency Converter (using data from currencylayer.com)\n")

    logging.debug('Updating available currencies set')
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

    rates = get_exchange_rates(api_key, CACHE_FILE)
    result = convert(from_cur, to_cur, amount, rates)

    print(f'\n{amount} {from_cur} = {result} {to_cur}')


if __name__ == "__main__":
    main()


# TODO: Github doesn't pull up the .env file. We need to come up with a script
#  for this situation, with a check for the presence
#  and a suggestion to enter the API key there.
