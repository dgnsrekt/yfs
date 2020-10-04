# Fuzzy Search Examples

## How to check if a symbol exists.

```python
from yfs import fuzzy_search

result = fuzzy_search("aapl")
print(result.json(indent=4))
```

!!! note
    * fuzzy_search returns a ValidSymbol or ValidSymbolList object.
    * Use the .json or .dict method to serialize these objects.

## How to search for a company by name.

```python
from yfs import fuzzy_search

results = fuzzy_search("Apple")
print(results)
```

## How to get the full search list.

```python
from yfs import fuzzy_search

results = fuzzy_search("Apple", first_ticker=False)
print(results.json(indent=4))

for ticker in results:
    print(ticker.json(indent=4))
```

!!! note
    * If the first_ticker argument is set to true fuzzy_search will return a ValidSymbolList.
    * ValidSymbolList is an iterable list of ValidSymbol objects.

## How to search and filter by region or asset type.

### Lets check for equities Tesla has listed in south america.

```python
from yfs import fuzzy_search
from yfs import ExchangeTypes

result = fuzzy_search("TESLA", first_ticker=False, exchange_type=ExchangeTypes.south_america)
print(result)
```

### Lets find ETF's with bull in the name.

```python
from pprint import pprint

from yfs import fuzzy_search
from yfs import ExchangeTypes
from yfs import AssetTypes

results = fuzzy_search(
    "bull",
    first_ticker=False,
    asset_type=AssetTypes.ETF,
    exchange_type=ExchangeTypes.united_states,
)
print(results.json(indent=4))

# Getting tired of json. let use dictionaries!
for ticker in results:
    pprint(ticker.dict())
```

!!! note
    * You can filter by asset_type by using the `AssetTypes` enum.

## How to filter symbols post lookup.

```python
from pprint import pprint

from yfs import fuzzy_search
from yfs import ExchangeTypes
from yfs import AssetTypes
from yfs import get_summary_page

results = fuzzy_search("AMZN", first_ticker=False, use_filter=False)
pprint(results.dict())

# Lets get the US indices with AMZN in the name.
index_only = results.filter_symbols(ExchangeTypes.united_states, AssetTypes.INDEX)
pprint(index_only.dict())

# Now lets get the summary pages of all the amazon listing in south america.
south_american_equities = results.filter_symbols(ExchangeTypes.south_america, AssetTypes.EQUITY)
for equity in south_american_equities:
    page = get_summary_page(equity.symbol)
    pprint(page.dict())
```

!!! note
    * Set first_ticker and use_filter arguments to false to allow filtering post return.
