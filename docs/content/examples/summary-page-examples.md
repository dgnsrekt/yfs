# Summary Page Examples

## How to get a single summary page.

```python
from yfs import get_summary_page  

result = get_summary_page("TSLA")
print(result.json(indent=4))
```

!!! note
    The get_summary_page function returns a single SummaryPage object. You can serialize the SummaryPage object to json or a dictionary with the .json() and .dict() methods.

## How to get multiple quotes from the summary page without threads.

```python
from yfs import get_multiple_summary_pages

COLUMNS = ["open", "high", "low", "close", "volume"]

search_items = ["TSLA", "GOOGLE", "appl", "aapl"]

results = get_multiple_summary_pages(search_items)
print(results.dataframe[COLUMNS])
```

!!! note
    You can pass company names too. This function will do a symbol look up for you using fuzzy_search. The get_multiple_summary_pages returns a SummaryPageGroup which you can serialize to a pandas dataframe.

## How to get multiple quotes from the summary page with threads.

```python
from yfs import get_multiple_summary_pages

COLUMNS = ["open", "high", "low", "close", "volume"]

search_items = ["TSLA", "GOOGLE", "appl", "aapl"]

results = get_multiple_summary_pages(search_items, with_threads=True, thread_count=5)

print(results.dataframe[COLUMNS])
```
