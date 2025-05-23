from pathlib import Path
from bs4 import BeautifulSoup
import logging


logger = logging.getLogger(__name__)


def parse_currency_codes_from_html(file_name):
    """ Parses an HTML file with a currency table and returns
    a set of currency codes. Should be called from main.py if needed."""
    logging.info("Started parser function")
    file_path = Path(__file__).parent / file_name  # This should be written as an instruction in README

    with open(file_path, 'r', encoding='utf-8') as f:
        logging.info(f'{file_name} opened successfully')
        soup = BeautifulSoup(f.read(), 'html.parser')

    codes = set()
    for td in soup.find_all('td'):
        code = td.get_text(strip=True).upper()
        if len(code) == 3 and code.isalpha():
            logging.debug('Suitable data available')
            codes.add(code)

    return codes
