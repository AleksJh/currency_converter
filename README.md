![CI Status](https://github.com/AleksJh/currency_converter/actions/workflows/ci.yml/badge.svg?branch=dev)

This program is build with poetry. To run it use:
$ poetry run python main.py

This program is originally designed to work with a free API key, which has some limitations. 
For example, it only provides access to USD->other rates. The program gets around this with a simple equation.

https://currencylayer.com/

List of available currencies on site is being parsed from file
"src/currency_app/cl-currencies-table.txt"
If you get a new file from original web page with updates, don't forget
to place it in the right directory - src/currency_app/
And if that file has another name, be sure that you replace it in
main.py's valid_currency_codes_update() function.
