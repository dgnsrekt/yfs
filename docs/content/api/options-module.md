> Contains the classes and functions for scraping a yahoo finance option page.

<a name="options.ContractExpiration"></a>
## `ContractExpiration`

> Contract Expiration.
> 
> **Attributes**:
> 
> - `symbol` _str_ - Ticker symbol.
> - `timestamp` _str_ - timestamp of expiration date.
> - `expiration_date` _DateTime_ - Datetime of expiration date.
>   
> 
> **Notes**:
> 
>   This class inherits from the pydantic BaseModel which allows for the use
>   of .json() and .dict() for serialization to json strings and dictionaries.
>   
> - `.json()` - Serialize to a JSON object.
> - `.dict()` - Serialize to a dictionary.

<a name="options.ContractExpiration.convert_to_datetime"></a>
#### `convert_to_datetime`

```python
 | def convert_to_datetime(cls, value: str) -> DateTime
```

> Convert expiration timestamp to datetime.

<a name="options.ContractExpiration.__lt__"></a>
#### `__lt__`

```python
 | def __lt__(other: "ContractExpiration") -> Optional["ContractExpiration"]
```

> Compare expiration_dates for sorting.

<a name="options.ContractExpirationList"></a>
## `ContractExpirationList`

> Contains Multiple Expirations.
> 
> **Attributes**:
> 
>   expiration_list List[ContractExpiration]: multiple expirations.
>   
> 
> **Notes**:
> 
>   This class inherits from the pydantic BaseModel which allows for the use
>   of .json() and .dict() for serialization to json strings and dictionaries.
>   
> - `.json()` - Serialize to a JSON object.
> - `.dict()` - Serialize to a dictionary.

<a name="options.ContractExpirationList.sort_dates"></a>
#### `sort_dates`

```python
 | def sort_dates(cls, values: List[ContractExpiration]) -> List[ContractExpiration]
```

> Sort expiration_list by date.

<a name="options.ContractExpirationList.filter_expirations_after"></a>
#### `filter_expirations_after`

```python
 | def filter_expirations_after(after: DateTime) -> None
```

> Filter out any expiration dates prior to the after date.
> 
> **Arguments**:
> 
> - `after` _DateTime_ - datetime to filter.
>   
> 
> **Example**:
> 
>   |Input                      | Args         |Output            |
>   |---------------------------|--------------|------------------|
>   |[01JAN19, 01FEB19, 01MAR19]|after: 15JAN19|[01FEB19, 01MAR19]|

<a name="options.ContractExpirationList.filter_expirations_before"></a>
#### `filter_expirations_before`

```python
 | def filter_expirations_before(before: DateTime) -> None
```

> Filter out any expiration dates post the before filter date.
> 
> **Arguments**:
> 
> - `before` _DateTime_ - datetime to filter.
>   
> 
> **Example**:
> 
>   |Input                      | Args          |Output   |
>   |---------------------------|---------------|---------|
>   |[01JAN19, 01FEB19, 01MAR19]|before: 15JAN19|[01JAN19]|

<a name="options.ContractExpirationList.filter_expirations_between"></a>
#### `filter_expirations_between`

```python
 | def filter_expirations_between(after: DateTime, before: DateTime) -> None
```

> Filter dates within a range.
> 
> **Arguments**:
> 
> - `after` _DateTime_ - datetime to filter.
> - `before` _DateTime_ - datetime to filter.
>   
> 
> **Example**:
> 
>   |Input                      | Args                         |Output            |
>   |---------------------------|------------------------------|------------------|
>   |[01JAN19, 01FEB19, 01MAR19]|after: 15JAN19,before: 15JAN19|[01FEB19, 01MAR19]|

<a name="options.ContractExpirationList.filter_expirations_after_days"></a>
#### `filter_expirations_after_days`

```python
 | def filter_expirations_after_days(days: int) -> None
```

> Filter expirations only allowing expirations after n days.
> 
> **Arguments**:
> 
> - `days` _int_ - Number of days to start filtering from. All expirations
>   after these days will be filtered out.

<a name="options.ContractExpirationList.filter_expirations_before_days"></a>
#### `filter_expirations_before_days`

```python
 | def filter_expirations_before_days(days: int) -> None
```

> Filter expiration only allowing expirations before n days.
> 
> **Arguments**:
> 
> - `days` _int_ - Number of days to start filtering from. All expirations
>   before these days will be filtered out.

<a name="options.ContractExpirationList.filter_expirations_between_days"></a>
#### `filter_expirations_between_days`

```python
 | def filter_expirations_between_days(after_days: Optional[int] = None, before_days: Optional[int] = None) -> None
```

> Filter expiration only allowing expirations between a range of days.
> 
> **Arguments**:
> 
> - `after_days` _int_ - Number of days to start filtering from. All expirations
>   after these days will be filtered out.
> - `before_days` _int_ - Number of days to start filtering from. All expirations
>   before these days will be filtered out.

<a name="options.ContractExpirationList.__len__"></a>
#### `__len__`

```python
 | def __len__() -> int
```

> Lenght of the expiration_list.

<a name="options.ContractExpirationList.__iter__"></a>
#### `__iter__`

```python
 | def __iter__() -> Iterable
```

> Iterate over the expirations_list.

<a name="options.ContractExpirationList.__add__"></a>
#### `__add__`

```python
 | def __add__(other: "ContractExpirationList") -> Optional["ContractExpirationList"]
```

> Combine two ContractExpirationLists.

<a name="options.OptionContractType"></a>
## `OptionContractType`

> Enum for option contacts.

<a name="options.OptionContract"></a>
## `OptionContract`

> Represents a Option Contract.
> 
> **Attributes**:
> 
> - `symbol` _str_ - Ticker symbol
> - `contract_type` _OptionContractType_ - Call or Put
>   
> - `timestamp` _str_ - Raw timestamp scraped from yahoo finance. This string is left
>   untouched to make sure there is no issues with building a URL.
> - `expiration_date` _DateTime_ - Converted from the timestamp. This allows allows
>   sorting and filtering.
> - `in_the_money` _bool_ - True if strike price is ITM else False.
>   
> - `contract_name` _str_ - Contract Name.
> - `last_trade_date` _DateTime_ - Date of last trade.
> - `strike` _float_ - Contracts strike price.
> - `last_price` _float_ - Last price of a transaction between a buyer and a seller.
>   
> - `bid` _float_ - Last bid price.
> - `ask` _float_ - Last ask price.
>   
> - `change` _float_ - Price change in dollars.
> - `percent_change` _float_ - Percentage change in dollars.
> - `volume` _int_ - Volume
> - `open_interest` _int_ - Number of contracts opened.
> - `implied_volatility` _float_ - Contracts IV.
>   
> 
> **Notes**:
> 
>   This class inherits from the pydantic BaseModel which allows for the use
>   of .json() and .dict() for serialization to json strings and dictionaries.
>   
> - `.json()` - Serialize to a JSON object.
> - `.dict()` - Serialize to a dictionary.

<a name="options.OptionsChain"></a>
## `OptionsChain`

> Chain of option contracts with the same expiration date.
> 
> **Attributes**:
> 
> - `symbol` _str_ - Company symbol.
> - `expiration_date` _DateTime_ - Contracts expiration date.
> - `chain` _List[OptionContract]_ - List of OptionContracts
>   
> 
> **Notes**:
> 
>   This class inherits from the pydantic BaseModel which allows for the use
>   of .json() and .dict() for serialization to json strings and dictionaries.
>   
> - `.json()` - Serialize to a JSON object.
> - `.dict()` - Serialize to a dictionary.

<a name="options.OptionsChain.dataframe"></a>
#### `dataframe`

```python
 | def dataframe() -> DataFrame
```

> Return a dataframe of the option chain.

<a name="options.OptionsChain.calls"></a>
#### `calls`

```python
 | def calls() -> "OptionsChain"
```

> Return a OptionChain with only call contracts.

<a name="options.OptionsChain.puts"></a>
#### `puts`

```python
 | def puts() -> "OptionsChain"
```

> Return a OptionChain with only put contracts.

<a name="options.OptionsChain.__len__"></a>
#### `__len__`

```python
 | def __len__() -> int
```

> Return the number of OptionContracts in the OptionChain.

<a name="options.MutipleOptionChains"></a>
## `MutipleOptionChains`

> Multiple Option Chains with multiple expiration date.
> 
> **Attributes**:
> 
> - `option_chain_list` _List[OptionsChain]_ - List of option chains.
> - `contract_expiration_list` _ContractExpirationList_ - List of expirations.
>   
> 
> **Notes**:
> 
>   This class inherits from the pydantic BaseModel which allows for the use
>   of .json() and .dict() for serialization to json strings and dictionaries.
>   
> - `.json()` - Serialize to a JSON object.
> - `.dict()` - Serialize to a dictionary.

<a name="options.MutipleOptionChains.dataframe"></a>
#### `dataframe`

```python
 | def dataframe() -> DataFrame
```

> Return a dataframe of multiple option chains.

<a name="options.MutipleOptionChains.calls"></a>
#### `calls`

```python
 | def calls() -> "MutipleOptionChains"
```

> Return a MutipleOptionChains object with only call contracts.

<a name="options.MutipleOptionChains.puts"></a>
#### `puts`

```python
 | def puts() -> "MutipleOptionChains"
```

> Return a MutipleOptionChains object with only put contracts.

<a name="options.MutipleOptionChains.__len__"></a>
#### `__len__`

```python
 | def __len__() -> int
```

> Return the number of option chains.

<a name="options.MutipleOptionChains.__iter__"></a>
#### `__iter__`

```python
 | def __iter__() -> Iterable
```

> Iterate over option chain list.

<a name="options.MutipleOptionChains.__add__"></a>
#### `__add__`

```python
 | def __add__(other: "MutipleOptionChains") -> Optional["MutipleOptionChains"]
```

> Concatenate MutipleOptionChains.

<a name="options.get_table_elements"></a>
#### `get_table_elements`

```python
def get_table_elements(html: HTML) -> Tuple[HTML, HTML]
```

> Parse call and put HTML table elements.
> 
> **Arguments**:
> 
> - `html` _HTML_ - HTML element with call and put data.
>   
> 
> **Returns**:
> 
>   Tuple of found call and put html elements.

<a name="options.parse_option_table"></a>
#### `parse_option_table`

```python
def parse_option_table(contract_expiration: ContractExpiration, contract_type: OptionContractType, options_table: HTML) -> List[OptionContract]
```

> Parse and clean fields and rows of a options table HTML element.
> 
> **Arguments**:
> 
> - `contract_expiration` _ContractExpiration_ - Used to pass ContractExpiration data
>   to the returned OptionContract object.
> - `contract_type` _OptionContractType_ - Call or Put
> - `options_table` _HTML_ - HTML element with raw options table data.
>   
> 
> **Returns**:
> 
>   A list of OptionContracts parsed from the html options_table.

<a name="options.get_option_expirations"></a>
#### `get_option_expirations`

```python
def get_option_expirations(symbol: str, **kwargs) -> Optional[ContractExpirationList]
```

> Get and parse option expiration data for the selected symbol.
> 
> **Arguments**:
> 
> - `symbol` _str_ - Ticker symbol.
> - `kwargs` - requestor kwargs (session, proxies, and timeout)
>   
> 
> **Returns**:
> 
>   ContractExpirationList

<a name="options.OptionPageNotFound"></a>
## `OptionPageNotFound`

> Raised when options page data is not found.

<a name="options.get_options_page"></a>
#### `get_options_page`

```python
def get_options_page(symbol: str, after_days: int = None, before_days: int = None, first_chain: bool = False, use_fuzzy_search: bool = True, page_not_found_ok: bool = False, **kwargs, ,) -> Optional[Union[OptionsChain, MutipleOptionChains]]
```

> Get options data from options page.
> 
> **Arguments**:
> 
> - `symbol` _str_ - Ticker symbol
> - `after_days` _int_ - Number of days to start filtering from. All expirations
>   after these days will be filtered out.
> - `before_days` _int_ - Number of days to start filtering from. All expirations
>   before these days will be filtered out.
> - `first_chain` _bool_ - If True returns first chain. Else returns all found chains
>   within search range.
> - `use_fuzzy_search` _bool_ - If True does a symbol lookup validation prior
>   to requesting options page data.
> - `page_not_found_ok` _bool_ - If True Returns None when page is not found.
> - `**kwargs` - requestor kwargs (session, proxies, and timeout)
>   
> 
> **Returns**:
> 
> - `OptionsChain` - If first_chain is set to True the first found OptionsChain
>   within the after_days and before_days range is returned.
>   This is all option contracts from a single expiration and symbol.
> - `MultipleOptionChains` - If first_chain is set to False all OptionsChains within
>   the after_days and before_days range are returned. This can have
>   multiple expirations. Even if one expiration date found
>   the MultipleOptionChains object is returned.
> - `None` - If no contracts are found and page_not_found_ok is True.
>   
> 
> **Raises**:
> 
> - `OptionPageNotFound` - If page_not_found_ok is False and the Options page is not found.

