> Contains the classes and functions for using the yahoo finance search.

<a name="lookup.ExchangeNotFoundError"></a>
## `ExchangeNotFoundError`

> Raised when an exchange is not found.

<a name="lookup.AssetTypeNotFoundError"></a>
## `AssetTypeNotFoundError`

> Raised when an assset type is not found.

<a name="lookup.ValidSymbol"></a>
## `ValidSymbol`

> A valid symbol reponse from the yahoo finance quote lookup search bar.
> 
> **Attributes**:
> 
> - `symbol` _str_ - A valid ticker symbol abbreviation.
> - `name` _str_ - The company name.
> - `exchange` _st_ - A valid market exchange.
>   The exchange str will be validated against all of the valid exchange
>   enums found in the yfs.exchanges module.
> - `asset_type` _str_ - A valid asset type.
>   The asset type will be validated against the
>   yfs.asset_types.AssetTypes enum.
>   
> 
> **Example**:
> 
> ```python
> {
>     "symbol": "AAPL",
>     "name": "Apple Inc.",
>     "exchange": "NASDAQ",
>     "asset_type": "Equity"
> }
> ```
> 
> **Notes**:
> 
>   This class inherits from the pydantic BaseModel which allows for the use
>   of .json() and .dict() for serialization to json strings and dictionaries.
>   
> - `.json()` - Serialize to a JSON object.
> - `.dict()` - Serialize to a dictionary.

<a name="lookup.ValidSymbol.check_exchange"></a>
#### `check_exchange`

```python
 | def check_exchange(cls, value: str) -> str
```

> Check if the exchange is in one of the valid yfs.exchanges enums.
> 
> **Raises**:
> 
> - `ExchangeNotFoundError` - If the exchange is not one yfs.exchanges enums
>   and if the RAISE_ERROR_ON_UNKOWN_EXCHANGE_OR_ASSET environmental variable
>   is set to True. (Default) is False.

<a name="lookup.ValidSymbol.check_type"></a>
#### `check_type`

```python
 | def check_type(cls, value: str) -> str
```

> Check if the asset_type is one of the valid yfs.asset_types enum.
> 
> **Raises**:
> 
> - `AssetTypeNotFoundError` - If the asset is not found in yfs.asset_types enum
>   and if the RAISE_ERROR_ON_UNKOWN_EXCHANGE_OR_ASSET environmental variable
>   is set to True. (Default) is False.

<a name="lookup.ValidSymbolList"></a>
## `ValidSymbolList`

> A list of symbol reponses from the yahoo finance quote lookup search bar.
> 
> **Attributes**:
> 
> - `symbols` _ValidSymbol_ - A list of ValidSymbol's.
>   
> 
> **Notes**:
> 
>   This class inherits from the pydantic BaseModel which allows for the use
>   of .json() and .dict() for serialization to json strings and dictionaries.
>   
> - `.json()` - Serialize to a JSON object.
> - `.dict()` - Serialize to a dictionary.

<a name="lookup.ValidSymbolList.__getitem__"></a>
#### `__getitem__`

```python
 | def __getitem__(index: int) -> Optional[ValidSymbol]
```

> Return ValidSymbol at index position.

<a name="lookup.ValidSymbolList.__len__"></a>
#### `__len__`

```python
 | def __len__() -> int
```

> Return the amount of symbols.

<a name="lookup.ValidSymbolList.__iter__"></a>
#### `__iter__`

```python
 | def __iter__() -> Iterable
```

> Iterate over ValidSymbol objects.

<a name="lookup.ValidSymbolList.filter_symbols"></a>
#### `filter_symbols`

```python
 | def filter_symbols(exchange_type: VALID_EXCHANGE_UNION, asset_type: AssetTypes) -> "ValidSymbolList"
```

> Filter symbols by exchange and asset type.
> 
> **Arguments**:
> 
> - `exchange_type` - A valid exchange enum. Example: yfs.exchanges.UnitedStatesExchanges
> - `asset_type` - A valid asset type. Example: yfs.asset_types.AssetTypes.EQUITY
>   
> 
> **Returns**:
> 
> - `ValidSymbolList` - A new ValidSymbolList with symbols within the exchange and
>   asset filters.

<a name="lookup.fuzzy_search"></a>
#### `fuzzy_search`

```python
def fuzzy_search(quote_lookup: str, exchange_type: VALID_EXCHANGE_UNION = UnitedStatesExchanges, asset_type: AssetTypes = AssetTypes.EQUITY, first_ticker: bool = True, use_filter: bool = False, **kwargs, ,) -> Optional[Union[ValidSymbol, ValidSymbolList]]
```

> Lookup and validate symbols or company names.
> 
> **Examples**:
> 
> ```python
> results = fuzzy_search("apple", first_ticker=False)
> print(results.json(indent=4))
> ```
>   
> ```json
> {
>     "symbols": [
>         {
>             "symbol": "AAPL",
>             "name": "Apple Inc.",
>             "exchange": "NASDAQ",
>             "asset_type": "Equity"
>         },
>         {
>             "symbol": "APLE",
>             "name": "Apple Hospitality REIT, Inc.",
>             "exchange": "NYSE",
>             "asset_type": "Equity"
>         },
>         ...
>     ]
> }
> ```
>   
> ```python
> result = fuzzy_search("aapl", first_ticker=True)
> print(result.json(indent=4))
> ```
>   
> ```json
> {
>     "symbol": "AAPL",
>     "name": "Apple Inc.",
>     "exchange": "NASDAQ",
>     "asset_type": "Equity"
> }
> ```
>   
> 
> **Arguments**:
> 
> - `quote_lookup` - The company name or symbol to search for.
> - `exchange_type` - One of the yfs.exchanges enums. Default is UnitedStatesExchanges
> - `asset_type` - One of the yfs.asset_type.AssetTypes. Default is AssetTypes.EQUITY
> - `first_ticker` - If set to true returns the first ValidSymbol in the ValidSymbolList.
>   This is normally the best recommended match from the yahoo finance quote lookup.
> - `**kwargs` - pass session, proxies, and timeout to the requestor
>   
> 
> **Returns**:
> 
> - `ValidSymbol` - If first_ticker is set to true and a valid ticker response is found.
> - `ValidSymbolList` - if first_ticker is set to false and a list of valid ticker
>   responses are found.
> - `None` - If the yahoo finance quote lookup search returns an empty response or if the
>   response did not meet the exchange and asset type filtering.
>   
> 
> **Raises**:
> 
> - `ExchangeNotFoundError` - If a exchange is found which has not been implemented in one of the
>   yfs.exchanges enums. If this error is raised please raise an issue on github with the
>   output.
> - `AssetTypeNotFoundError` - If an asset type is not found in the
>   yfs.asset_types.AssetTypes enum. If this error is raised please raise and issue on
>   github with the output.

