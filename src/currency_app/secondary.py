import logging
import json
from pathlib import Path


logger = logging.getLogger(__name__)


def parse_currency_codes_from_json(file_name: str) -> set[str]:
    """Parses a JSON file of currency objects and
        returns a set of currency codes."""
    logging.debug("Started JSON parser function")
    file_path = Path(__file__).parent / file_name

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            logging.debug(f"{file_name} opened successfully")
            data = json.load(f)
    except FileNotFoundError:
        logging.exception(f"File not found: {file_name}")
        return set()
    except json.JSONDecodeError as e:
        logging.exception(f"JSON parsing error: {e}")
        return set()

    codes = {entry["code"].upper() for entry in data if "code" in entry and
             len(entry["code"]) == 3}

    logging.info(f"Parsed {len(codes)} currency codes from JSON")
    return codes
