from prompt_toolkit import prompt
from yfs.statistics import get_statistics_page

from requests import Session

import time

while True:
    print("Use 'exit' to end.")
    print("Type one symbol/company name or multiple separated by spaces.")

    session = Session()

    user_input = prompt(":> ").strip()

    if user_input == "exit":
        break

    symbols = user_input.split(" ")

    output = None

    if len(symbols) == 1:
        output = get_statistics_page(
            symbols[0], use_fuzzy_search=True, page_not_found_ok=True, session=session
        )

    if output:
        print(output.json(indent=4))
        print(output.valuation_measures.dataframe)

    else:
        print("nothing found")
