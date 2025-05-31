![CI Status](https://github.com/AleksJh/currency_converter/actions/workflows/ci.yml/badge.svg?branch=dev)

---

# Currency Converter Application

This application is built using **Poetry**, a dependency management tool for Python.

## Getting Started
---
1.  **Install Poetry**: If you don't have Poetry installed, follow the instructions on their official website.
2.  **Run the Application**: Once Poetry is set up, you can run the program using the following command from your project's root directory:

    ```bash
    $ poetry run python path_to_/main.py
    ```

---

## API Usage and Limitations
---
This program is primarily designed to work with a **free API key** from [CurrencyLayer](https://currencylayer.com/). Free API keys typically have limitations, such as only providing exchange rates from USD to other currencies. The program intelligently handles this by using a simple equation to calculate other cross-currency rates.

---

## Currency Data
---
The list of available currencies is parsed from the file located at:

`src/currency_app/cl-currencies.json`

**Important Notes:**

* If you obtain an updated currency list file, make sure to place it in the correct directory: `src/currency_app/`.
* If the new file has a different name, you'll need to update the `valid_currency_codes_update()` function in `main.py` to reflect the new filename.