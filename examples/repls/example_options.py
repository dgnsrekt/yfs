from yfs.options import get_options_page

from prompt_toolkit import prompt
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

        chains = get_options_page(
            user_input, use_fuzzy_search=True, first_chain=True, after_days=30, before_days=120
        )
        if chains:

            print(len(chains))
            print(chains.dataframe)
            print(chains.puts.dataframe)
            print(chains.calls.dataframe)

        else:
            print("nothing found")

        # chains = chains + chains
        # print(chains.calls.json(indent=4))
    # elif len(symbols) > 1:

    # if output:
    # print(output.json(indent=4))

    else:
        print("nothing found")

    time.sleep(1)
