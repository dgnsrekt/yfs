from yfs import fuzzy_search
from yfs import ExchangeTypes
from yfs import AssetTypes
from yfs import get_summary_page

from pprint import pprint

# How to check if a symbol exists.

result = fuzzy_search("aapl")
print(result.json(indent=4))

# How to search for a company by name.

results = fuzzy_search("Apple")
print(results)

# How to get the full response list.

results = fuzzy_search("Apple", first_ticker=False)
print(results.json(indent=4))

for ticker in results:
    print(ticker.json(indent=4))

"""fuzzy_search can return a ValidSymbol or ValidSymbolList.
If first_ticker is True (the default value) it will return a single ValidSymbol.
If the first_ticker is False it will return a ValidSymbolList.
The ValidSymbolList is an iterable list of ValidSymbol(s).
Additionally, you can use the .json and .dict on both the ValidSymbolList, and ValidSymbol.
"""

# How to do a lookup in a different exchange region.
# Lets check for all the equities Tesla has listed in south america.

result = fuzzy_search("TESLA", first_ticker=False, exchange_type=ExchangeTypes.south_america)
print(result)

# Lets find all the ETFs with bull in the name.
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

# Want to filter post search set use_filter to False and use the ValidSymbol.filter_symbols method.
results = fuzzy_search("AMZN", first_ticker=False, use_filter=False)
pprint(results.dict())

# Lets get the US indices with AMZN in the name.
index_only = results.filter_symbols(ExchangeTypes.united_states, AssetTypes.INDEX)
pprint(index_only.dict())

# Now lets get the summary pages of all the amazon equities listing in south america.
south_american_equities = results.filter_symbols(ExchangeTypes.south_america, AssetTypes.EQUITY)
for equity in south_american_equities:
    page = get_summary_page(equity.symbol)
    pprint(page.dict())
