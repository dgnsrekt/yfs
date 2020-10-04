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
> - `trailing_pe` _float_ - relative valuation multiple that is based on the
>   last 12 months of actual earnings
> - `forward_pe` _float_ - Version of the ratio of price-to-earnings that uses
>   forecasted earnings for the P/E calculation.
> - `peg_ratio_five_year_expected` _float_ - A valuation metric for determining
>   the relative trade-off between the price of a stock, the EPS, and the
>   company's expected growth.
> - `price_sales_ttm` _float_ - Trailing Twelve Months price to sales ratio.
>   price_book_mrq (float):
>   enterprise_revenue (float):
>   enterprise_ebitda (float):
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

> Valuation Measures Table as a dataframe.

<a name="statistics.FinancialHighlights"></a>
## `FinancialHighlights`

> Financial highlights section of a yahoo finance statistics page.
> 
> **Attributes**:
> 
>   fiscal_year_ends (Date):
>   most_recent_quarter_mrq (Date):
>   
>   profit_margin (float):
>   operating_margin_ttm (float):
>   
>   return_on_assets_ttm (float):
>   return_on_equity_ttm (float):
>   
>   revenue_ttm (int):
>   revenue_per_share_ttm (float):
>   quarterly_revenue_growth_yoy (float):
>   gross_profit_ttm (int):
>   ebitda (int):
>   net_income_avi_to_common_ttm (int):
>   diluted_eps_ttm (float):
>   quarterly_earnings_growth_yoy (float):
>   
>   total_cash_mrq (int):
>   total_cash_per_share_mrq (float):
>   total_debt_mrq (int):
>   total_debt_equity_mrq (float):
>   current_ratio_mrq (float):
>   book_value_per_share_mrq (float):
>   
>   levered_free_cash_flow_ttm (int):
>   operating_cash_flow_ttm (int):
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
>   beta_five_year_monthly (float):
>   
>   fifty_two_week_change (float):
>   sp500_fifty_two_week_change (float):
>   fifty_two_week_high (float):
>   fifty_two_week_low (float):
>   fifty_day_moving_average (float):
>   two_hundred_day_moving_average (float):
>   
>   average_three_month_volume (int):
>   average_ten_day_volume (int):
>   shares_outstanding (int):
>   float (int):
>   percent_held_by_insiders (float):
>   percent_held_by_institutions (float):
>   
>   shares_short (int):
>   shares_short_date (Date):
>   short_ratio (float):
>   short_ratio_date (Date):
>   short_percent_of_float (float):
>   short_percent_of_float_date (Date):
>   short_percent_of_shares_outstanding (float):
>   short_percent_of_shares_outstanding_date (Date):
>   shares_short_prior_month (int):
>   shares_short_prior_month_date (Date):
>   
>   forward_annual_dividend_rate (float):
>   forward_annual_dividend_yield (float):
>   trailing_annual_dividend_rate (float):
>   trailing_annual_dividend_yield (float):
>   
>   five_year_average_dividend_yield (float):
>   
>   payout_ratio (float):
>   dividend_date (Date):
>   exdividend_date (Date):
>   last_split_factor (str):
>   last_split_date (Date):
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
> - `html` - Html element contatining valuation table data.
> - `period_type` _PeriodType_ - The period to be parsed. Only quarterly is currently supported.
>   
> 
> **Returns**:
> 
> - `ValuationMeasuresTable` - If data is found.
> - `None` - No data avaliable.

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
> - `symbol` _st_ - Ticker Symbol
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

<a name="statistics.StatisticsPageGroup"></a>
## `StatisticsPageGroup`

> Multiple Statistics Pages Group together.
> 
> **Attributes**:
> 
> - `pages` - Multiple StatisticsPage objects. A page per symbol requested.
>   
> 
> **Notes**:
> 
>   This class inherits from the pydantic BaseModel which allows for the use
>   of .json() and .dict() for serialization to json strings and dictionaries.
>   
> - `.json()` - Serialize to a JSON object.
> - `.dict()` - Serialize to a dictionary.

<a name="statistics.StatisticsPageGroup.dataframe"></a>
#### `dataframe`

```python
 | def dataframe() -> DataFrame
```

> Return a dataframe of multiple statistics pages.

<a name="statistics.StatisticsPageNotFound"></a>
## `StatisticsPageNotFound`

> Raised when statistics page data is not found.

<a name="statistics.get_statistics_page"></a>
#### `get_statistics_page`

```python
def get_statistics_page(symbol: str, use_fuzzy_search: bool = True, page_not_found_ok: bool = False, **kwargs, ,) -> Optional[StatisticsPage]
```

> Get statistics page data.
> 
> **Arguments**:
> 
> - `symbol` _str_ - Ticker symbol
> - `use_fuzzy_search` _bool_ - If True does a symbol lookup validation prior
>   to requesting options page data.
> - `page_not_found_ok` _bool_ - If True Returns None when page is not found.
> - `**kwargs` - requestor kwargs (session, proxies, and timeout)
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
> - `StatisticsPageNotFound` - When a page is not found and the page_not_found_ok arg is false.

