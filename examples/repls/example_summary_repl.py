from prompt_toolkit import prompt

from yfs.summary import get_summary_page, get_multiple_summary_pages
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
        output = get_summary_page(
            symbols[0], use_fuzzy_search=True, page_not_found_ok=True, session=session
        )

    elif len(symbols) > 1:
        output = get_multiple_summary_pages(symbols, with_threads=True, session=session)

        if output:
            output.sort()
            print(output.dataframe)

    if output:
        print(output.json(indent=4))

    else:
        print("nothing found")

    time.sleep(1)
