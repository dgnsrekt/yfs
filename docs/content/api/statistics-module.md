> Contains the classes and functions for scraping a yahoo finance statistics page.

<a name="statistics.PeriodType"></a>
## `PeriodType`

> Enum which describes the period the data represents.

<a name="statistics.Valuation"></a>
## `Valuation`

> Data representing the intrinsic value of an asset for a single date.
> 
> This is for one column of an entire valuation table.
> 
> **Attributes**:
> 
> - `date` _Date_ - Date of the valuation.
> - `period_type` _PeriodType_ - Annual, Quarterly, or Monthly.
> - `market_cap_intraday` _int_ - Calculated using shares_outstanding from the
>   most recently filed report.
> - `enterprise_value` _int_ - Measure of a company's total value.
> - `trailing_pe` _float_ - Relative valuation multiple that is based on the
>   last 12 months of actual earnings
> - `forward_pe` _float_ - Forward price-to-earnings (forward P/E) is a version of the
>   ratio of price-to-earnings (P/E) that uses forecasted earnings for the P/E calculation.
> - `peg_ratio_five_year_expected` _float_ - A valuation metric for determining
>   the relative trade-off between the price of a stock, the EPS, and the
>   company's expected growth.
> - `price_sales_ttm` _float_ - Trailing Twelve Months price to sales ratio.
> - `price_book_mrq` _float_ - todo
> - `enterprise_revenue` _float_ - todo
> - `enterprise_ebitda` _float_ - todo
>   
> 
> **Notes**:
> 
>   This class inherits from the pydantic BaseModel which allows for the use
>   of .json() and .dict() for serialization to json strings and dictionaries.
>   
> - `.json()` - Serialize to a JSON object.
> - `.dict()` - Serialize to a dictionary.

<a name="statistics.Valuation.Config"></a>
## `Config`

> Pydantic config.

<a name="statistics.ValuationMeasuresTable"></a>
## `ValuationMeasuresTable`

> Representing the entire Valuation Measures Table on a yahoo finance Statistics Page.
> 
> **Attributes**:
> 
> - `valuations` _List[Valuation]_ - A list of valuation objects.
>   
> 
> **Notes**:
> 
>   This class inherits from the pydantic BaseModel which allows for the use
>   of .json() and .dict() for serialization to json strings and dictionaries.
>   
> - `.json()` - Serialize to a JSON object.
> - `.dict()` - Serialize to a dictionary.

<a name="statistics.ValuationMeasuresTable.dataframe"></a>
#### `dataframe`

```python
 | def dataframe() -> DataFrame
```

> Return the Valuation Measures Table as a dataframe.

<a name="statistics.FinancialHighlights"></a>
## `FinancialHighlights`

> Financial highlights section of a yahoo finance statistics page.
> 
> **Attributes**:
> 
> - `fiscal_year_ends` _Date_ - todo
> - `most_recent_quarter_mrq` _Date_ - todo
>   
> - `profit_margin` _float_ - todo
> - `operating_margin_ttm` _float_ - todo
>   
> - `return_on_assets_ttm` _float_ - todo
> - `return_on_equity_ttm` _float_ - todo
>   
> - `revenue_ttm` _int_ - todo
> - `revenue_per_share_ttm` _float_ - todo
> - `quarterly_revenue_growth_yoy` _float_ - todo
> - `gross_profit_ttm` _int_ - todo
> - `ebitda` _int_ - todo
> - `net_income_avi_to_common_ttm` _int_ - todo
> - `diluted_eps_ttm` _float_ - todo
> - `quarterly_earnings_growth_yoy` _float_ - todo
>   
> - `total_cash_mrq` _int_ - todo
> - `total_cash_per_share_mrq` _float_ - todo
> - `total_debt_mrq` _int_ - todo
> - `total_debt_equity_mrq` _float_ - todo
> - `current_ratio_mrq` _float_ - todo
> - `book_value_per_share_mrq` _float_ - todo
>   
> - `levered_free_cash_flow_ttm` _int_ - todo
> - `operating_cash_flow_ttm` _int_ - todo
>   
> 
> **Notes**:
> 
>   This class inherits from the pydantic BaseModel which allows for the use
>   of .json() and .dict() for serialization to json strings and dictionaries.
>   
> - `.json()` - Serialize to a JSON object.
> - `.dict()` - Serialize to a dictionary.

<a name="statistics.TradingInformation"></a>
## `TradingInformation`

> Trading information section of a yahoo finance statistics page.
> 
> **Attributes**:
> 
> - `beta_five_year_monthly` _float_ - todo
>   
> - `fifty_two_week_change` _float_ - todo
> - `sp500_fifty_two_week_change` _float_ - todo
> - `fifty_two_week_high` _float_ - todo
> - `fifty_two_week_low` _float_ - todo
> - `fifty_day_moving_average` _float_ - todo
> - `two_hundred_day_moving_average` _float_ - todo
>   
> - `average_three_month_volume` _int_ - todo
> - `average_ten_day_volume` _int_ - todo
> - `shares_outstanding` _int_ - todo
> - `float` _int_ - todo
> - `percent_held_by_insiders` _float_ - todo
> - `percent_held_by_institutions` _float_ - todo
>   
> - `shares_short` _int_ - todo
> - `shares_short_date` _Date_ - todo
> - `short_ratio` _float_ - todo
> - `short_ratio_date` _Date_ - todo
> - `short_percent_of_float` _float_ - todo
> - `short_percent_of_float_date` _Date_ - todo
> - `short_percent_of_shares_outstanding` _float_ - todo
> - `short_percent_of_shares_outstanding_date` _Date_ - todo
> - `shares_short_prior_month` _int_ - todo
> - `shares_short_prior_month_date` _Date_ - todo
>   
> - `forward_annual_dividend_rate` _float_ - todo
> - `forward_annual_dividend_yield` _float_ - todo
> - `trailing_annual_dividend_rate` _float_ - todo
> - `trailing_annual_dividend_yield` _float_ - todo
>   
> - `five_year_average_dividend_yield` _float_ - todo
>   
> - `payout_ratio` _float_ - todo
> - `dividend_date` _Date_ - todo
> - `exdividend_date` _Date_ - todo
> - `last_split_factor` _str_ - todo
> - `last_split_date` _Date_ - todo
>   
> 
> **Notes**:
> 
>   This class inherits from the pydantic BaseModel which allows for the use
>   of .json() and .dict() for serialization to json strings and dictionaries.
>   
> - `.json()` - Serialize to a JSON object.
> - `.dict()` - Serialize to a dictionary.

<a name="statistics.parse_valuation_table"></a>
#### `parse_valuation_table`

```python
def parse_valuation_table(html: HTML, period_type: PeriodType = PeriodType.QUARTERLY) -> Optional[ValuationMeasuresTable]
```

> Parse and clean fields and rows of a valuation measures table HTML element.
> 
> **Arguments**:
> 
> - `html` - Html element containing valuation table data.
> - `period_type` _PeriodType_ - The period to be parsed. Only quarterly is currently supported.
>   
> 
> **Returns**:
> 
> - `ValuationMeasuresTable` - If data is found.
> - `None` - No data available.

<a name="statistics.parse_financial_highlights_table"></a>
#### `parse_financial_highlights_table`

```python
def parse_financial_highlights_table(html: HTML) -> Optional[FinancialHighlights]
```

> Parse and clean fields and rows of a financial highlights section of an HTML element.

<a name="statistics.parse_trading_information_table"></a>
#### `parse_trading_information_table`

```python
def parse_trading_information_table(html: HTML) -> Optional[TradingInformation]
```

> Parse and clean fields and rows of a trading information section of an HTML element.

<a name="statistics.StatisticsPage"></a>
## `StatisticsPage`

> Represents all data you can find on a yahoo finance statistics page.
> 
> **Attributes**:
> 
> - `symbol` _st_ - Ticker Symbol.
> - `quote` _Quote_ - Quote data from the quote header section.
> - `valuation_measures` _ValuationMeasuresTable_ - Valuation Measures Table section.
> - `financial_highlights` _FinancialHighlights_ - Financial Highlights section.
> - `trading_information` _TradingInformation_ - Trading Information section
>   
> 
> **Notes**:
> 
>   This class inherits from the pydantic BaseModel which allows for the use
>   of .json() and .dict() for serialization to json strings and dictionaries.
>   
> - `.json()` - Serialize to a JSON object.
> - `.dict()` - Serialize to a dictionary.

<a name="statistics.StatisticsPage.__lt__"></a>
#### `__lt__`

```python
 | def __lt__(other) -> bool
```

> Compare StatisticsPage objects to allow ordering by symbol.

<a name="statistics.StatisticsPageGroup"></a>
## `StatisticsPageGroup`

> Multiple Statistics Pages Group together.
> 
> **Attributes**:
> 
> - `pages` - Multiple StatisticsPage objects. A page for each symbol requested.
>   
> 
> **Notes**:
> 
>   This class inherits from the pydantic BaseModel which allows for the use
>   of .json() and .dict() for serialization to json strings and dictionaries.
>   
> - `.json()` - Serialize to a JSON object.
> - `.dict()` - Serialize to a dictionary.

<a name="statistics.StatisticsPageGroup.append"></a>
#### `append`

```python
 | def append(page: StatisticsPage) -> None
```

> Append a StatisticsPage to the StatisticsPageGroup.
> 
> **Arguments**:
> 
> - `page` _StatisticsPage_ - A StatisticsPage object to add to the group.

<a name="statistics.StatisticsPageGroup.symbols"></a>
#### `symbols`

```python
 | def symbols() -> List[str]
```

> List of symbols in the StatisticsPageGroup.

<a name="statistics.StatisticsPageGroup.sort"></a>
#### `sort`

```python
 | def sort() -> None
```

> Sort StatisticsPage objects by symbol.

<a name="statistics.StatisticsPageGroup.dataframe"></a>
#### `dataframe`

```python
 | def dataframe() -> DataFrame
```

> Return a dataframe of multiple statistics pages.

<a name="statistics.StatisticsPageGroup.__iter__"></a>
#### `__iter__`

```python
 | def __iter__() -> Iterable
```

> Iterate over StatisticsPage objects.

<a name="statistics.StatisticsPageGroup.__len__"></a>
#### `__len__`

```python
 | def __len__() -> int
```

> Length of StatisticsPage objects.

<a name="statistics.get_statistics_page"></a>
#### `get_statistics_page`

```python
def get_statistics_page(symbol: str, use_fuzzy_search: bool = True, page_not_found_ok: bool = False, **kwargs, ,) -> Optional[StatisticsPage]
```

> Get statistics page data.
> 
> **Arguments**:
> 
> - `symbol` _str_ - Ticker symbol.
> - `use_fuzzy_search` _bool_ - If True validates symbol prior to requesting options page data.
> - `page_not_found_ok` _bool_ - If True Returns None when page is not found.
> - `**kwargs` - Pass (session, proxies, and timeout) to the requestor function.
>   
> 
> **Returns**:
> 
> - `StatisticsPage` - When data is found.
> - `None` - No data is found and page_not_found_ok is True.
>   
> 
> **Raises**:
> 
> - `AttributeError` - When a page is not found and the page_not_found_ok arg is false.

<a name="statistics.get_multiple_statistics_pages"></a>
#### `get_multiple_statistics_pages`

```python
def get_multiple_statistics_pages(symbols: List[str], use_fuzzy_search: bool = True, page_not_found_ok: bool = True, with_threads: bool = False, thread_count: int = 5, progress_bar: bool = True, **kwargs, ,) -> Optional[StatisticsPageGroup]
```

> Get multiple statistics pages.
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
> - `StatisticsPageGroup` - When data is found.
> - `None` - No data is found and page_not_found_ok is True.
>   
> 
> **Raises**:
> 
> - `AttributeError` - When a page is not found and the page_not_found_ok arg is false.

