# SummaryPage Examples

from yfs import get_summary_page, get_multiple_summary_pages

## How to get a single summary page.
result = get_summary_page("TSLA")
print(result.json(indent=4))

# Note: get_summary_page returns a single SummaryPage object.
# You can serialize a SummaryPage object to .json or a .dict()

## How to a list of quotes from the summary page.
from yfs import get_summary_page, get_multiple_summary_pages

COLUMNS = ["open", "high", "low", "close", "volume"]

search_items = ["TSLA", "GOOGLE", "appl", "aapl"]

results = get_multiple_summary_pages(search_items)

print(results.dataframe[COLUMNS])

# Note: You can pass company names too.
# This function will do a symbol look up for you.
# The get_multiple_summary_pages returns a SummaryPageGroup which is serializable to a pandas dataframe.
