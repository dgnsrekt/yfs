# Statistics Page Examples

## How to get a single symbols statistics page.
```python
from yfs import get_statistics_page

result = get_statistics_page("AAPL")
print(result.json(indent=4))
```

## How to get multiple statistics pages without threads
```python
from yfs import get_multiple_statistics_pages

search_items = ["TSLA", "GOOGLE", "appl", "aapl"]

results = get_multiple_statistics_pages(search_items, with_threads=False)

print(results.dataframe)
```

## How to get multiple statistics pages with threads
```python
from yfs import get_multiple_statistics_pages

search_items = ["TSLA", "GOOGLE", "appl", "aapl"]

results = get_multiple_statistics_pages(search_items, with_threads=True, thread_count=5)

print(results.dataframe)
```
