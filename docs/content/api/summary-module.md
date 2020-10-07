> Contains the classes and functions for scraping a yahoo finance summary page.

<a name="summary.SummaryPage"></a>
## `SummaryPage`

> Data scraped from the yahoo finance summary page.
> 
> **Attributes**:
> 
> - `symbol` _str_ - Ticker Symbol
> - `name` _str_ - Ticker Name
>   
> - `quote` _Quote_ - Quote header section of the page.
>   
> - `open` _float_ - Open price.
> - `high` _float_ - Days high.
> - `low` _float_ - Days low.
> - `close` _float_ - Days close price.
>   
> - `change` _float_ - Dollar change in price.
> - `percent_change` _float_ - Percent change in price.
>   
> - `previous_close` _float_ - Previous days close price.
>   
> - `bid_price` _float_ - Bid price.
> - `bid_size` _int_ - Bid size.
>   
> - `ask_price` _float_ - Ask price.
> - `ask_size` _int_ - Ask size.
>   
> - `fifty_two_week_high` _float_ - High of the fifty two week range.
> - `fifty_two_week_low` _float_ - Low of the fifty two week range.
>   
> - `volume` _int_ - Volume.
> - `average_volume` _int_ - Average Volume.
>   
> - `market_cap` _int_ - Market capitalization.
>   
> - `beta_five_year_monthly` _float_ - Five year monthly prices benchmarked against the SPY.
> - `pe_ratio_ttm` _float_ - Share Price divided by Earnings Per Share trailing twelve months.
> - `eps_ttm` _float_ - Earnings per share trailing twelve months.
>   
> - `earnings_date` _Date_ - Estimated earnings report release date.
>   
> - `forward_dividend_yield` _float_ - Estimated dividend yield.
> - `forward_dividend_yield_percentage` _float_ - Estimated divided yield percentage.
> - `exdividend_date` _Date_ - Ex-Dividend Date.
>   
> - `one_year_target_est` _float_ - One year target estimation.
>   
> 
> **Notes**:
> 
>   This class inherits from the pydantic BaseModel which allows for the use
>   of .json() and .dict() for serialization to json strings and dictionaries.
>   
> - `.json()` - Serialize to a JSON object.
> - `.dict()` - Serialize to a dictionary.

<a name="summary.SummaryPage.__lt__"></a>
#### `__lt__`

```python
 | def __lt__(other) -> bool
```

> Compare SummaryPage objects to allow ordering by symbol.

<a name="summary.SummaryPageGroup"></a>
## `SummaryPageGroup`

> Group of SummaryPage objects from multiple symbols.
> 
> **Attributes**:
> 
>   pages (SummaryPage):
>   
> 
> **Notes**:
> 
>   This class inherits from the pydantic BaseModel which allows for the use
>   of .json() and .dict() for serialization to json strings and dictionaries.
>   
> - `.json()` - Serialize to a JSON object.
> - `.dict()` - Serialize to a dictionary.

<a name="summary.SummaryPageGroup.append"></a>
#### `append`

```python
 | def append(page: SummaryPage) -> None
```

> Append a SummaryPage to the SummaryPageGroup.
> 
> **Arguments**:
> 
> - `page` _SummaryPage_ - A SummaryPage object to add to the group.

<a name="summary.SummaryPageGroup.symbols"></a>
#### `symbols`

```python
 | def symbols() -> List[str]
```

> List of symbols in the SummaryPageGroup.

<a name="summary.SummaryPageGroup.sort"></a>
#### `sort`

```python
 | def sort() -> None
```

> Sort SummaryPage objects by symbol.

<a name="summary.SummaryPageGroup.dataframe"></a>
#### `dataframe`

```python
 | def dataframe() -> Optional[DataFrame]
```

> Return a dataframe of multiple SummaryPage objects.

<a name="summary.SummaryPageGroup.__iter__"></a>
#### `__iter__`

```python
 | def __iter__() -> Iterable
```

> Iterate over SummaryPage objects.

<a name="summary.SummaryPageGroup.__len__"></a>
#### `__len__`

```python
 | def __len__() -> int
```

> Length of SummaryPage objects.

<a name="summary.parse_summary_table"></a>
#### `parse_summary_table`

```python
def parse_summary_table(html: HTML) -> Optional[Dict]
```

> Parse data from summary table HTML element.

<a name="summary.SummaryPageNotFound"></a>
## `SummaryPageNotFound`

> Raised when summary page data is not found.

<a name="summary.get_summary_page"></a>
#### `get_summary_page`

```python
def get_summary_page(symbol: str, use_fuzzy_search: bool = True, page_not_found_ok: bool = False, **kwargs, ,) -> Optional[SummaryPage]
```

> Get summary page data.
> 
> **Arguments**:
> 
> - `symbol` _str_ - Ticker symbol.
> - `use_fuzzy_search` _bool_ - If True does a symbol lookup validation prior
>   to requesting summary page data.
> - `page_not_found_ok` _bool_ - If True Returns None when page is not found.
> - `**kwargs` - Pass (session, proxies, and timeout) to the requestor function.
>   
> 
> **Returns**:
> 
> - `SummaryPage` - When data is found.
> - `None` - No data is found and page_not_found_ok is True.
>   
> 
> **Raises**:
> 
> - `SummaryPageNotFound` - When a page is not found and the page_not_found_ok arg is false.

<a name="summary.get_multiple_summary_pages"></a>
#### `get_multiple_summary_pages`

```python
def get_multiple_summary_pages(symbols: List[str], use_fuzzy_search: bool = True, page_not_found_ok: bool = True, with_threads: bool = False, thread_count: int = 5, progress_bar: bool = True, **kwargs, ,) -> Optional[SummaryPageGroup]
```

> Get multiple summary pages.
> 
> **Arguments**:
> 
> - `symbols` _List[str]_ - Ticker symbols or company names.
> - `use_fuzzy_search` _bool_ - If True does a symbol lookup validation prior
>   to requesting data.
> - `page_not_found_ok` _bool_ - If True Returns None when page is not found.
> - `with_threads` _bool_ - If True uses threading.
> - `thread_count` _int_ - Number of threads to use if with_threads is set to True.
> - `**kwargs` - Pass (session, proxies, and timeout) to the requestor function.
> - `progress_bar` _bool_ - If True shows the progress bar else the progress bar
>   is not shown.
>   
> 
> **Returns**:
> 
> - `SummaryPageGroup` - When data is found.
> - `None` - No data is found and page_not_found_ok is True.
>   
> 
> **Raises**:
> 
> - `SummaryPageNotFound` - When a page is not found and the page_not_found_ok arg is false.

