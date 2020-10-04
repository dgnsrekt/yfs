"""Contains the classes and functions for scraping a yahoo finance statistics page."""

from collections import ChainMap
from enum import Enum
from typing import List, Optional

import numpy as np
import pandas
from pandas import DataFrame
from pendulum.date import Date
from pydantic import BaseModel as Base
from pydantic import Field
from requests_html import HTML

from .cleaner import cleaner, CommonCleaners, field_cleaner, table_cleaner
from .lookup import fuzzy_search
from .quote import parse_quote_header_info, Quote
from .requestor import requestor


class PeriodType(str, Enum):
    """Enum which describes the period the data represents."""

    ANNUALY = "Annual"
    QUARTERLY = "Quarterly"
    MONTHLY = "Monthly"


class Valuation(Base):
    """Data representing the intrinsic value of an asset for a single date.

    This is for one column of an entire valuation table.

    Attributes:
        date (Date): Date of the valuation.
        period_type (PeriodType): Annual, Quarterly, or Monthly.
        market_cap_intraday (int): Calculated using shares_outstanding from the
            most recently filed report.
        enterprise_value (int): Measure of a company's total value.
        trailing_pe (float): relative valuation multiple that is based on the
            last 12 months of actual earnings
        forward_pe (float): Version of the ratio of price-to-earnings that uses
            forecasted earnings for the P/E calculation.
        peg_ratio_five_year_expected (float): A valuation metric for determining
            the relative trade-off between the price of a stock, the EPS, and the
            company's expected growth.
        price_sales_ttm (float): Trailing Twelve Months price to sales ratio.
        price_book_mrq (float):
        enterprise_revenue (float):
        enterprise_ebitda (float):

    Notes:
        This class inherits from the pydantic BaseModel which allows for the use
        of .json() and .dict() for serialization to json strings and dictionaries.

        .json(): Serialize to a JSON object.
        .dict(): Serialize to a dictionary.
    """

    date: Date
    period_type: PeriodType

    market_cap_intraday: Optional[int] = Field(alias="market_cap_intraday_5")
    enterprise_value: Optional[int] = Field(alias="enterprise_value_3")
    trailing_pe: Optional[float] = Field(alias="trailing_p_e")
    forward_pe: Optional[float] = Field(alias="forward_p_e_1")
    peg_ratio_five_year_expected: Optional[float] = Field(alias="peg_ratio_five_year_expected_1")
    price_sales_ttm: Optional[float]
    price_book_mrq: Optional[float]
    enterprise_revenue: Optional[float] = Field(alias="enterprise_value_revenue_3")
    enterprise_ebitda: Optional[float] = Field(alias="enterprise_value_ebitda_6")

    _clean_dates = cleaner("date")(CommonCleaners.clean_date)

    _clean_common_values = cleaner(
        "market_cap_intraday",
        "enterprise_value",
        "trailing_pe",
        "forward_pe",
        "peg_ratio_five_year_expected",
        "price_sales_ttm",
        "price_book_mrq",
        "enterprise_revenue",
        "enterprise_ebitda",
    )(CommonCleaners.clean_common_values)

    class Config:
        """Pydantic config."""

        use_enum_values = True


class ValuationMeasuresTable(Base):
    """Representing the entire Valuation Measures Table on a yahoo finance Statistics Page.

    Attributes:
        valuations (List[Valuation]): A list of valuation objects.

    Notes:
        This class inherits from the pydantic BaseModel which allows for the use
        of .json() and .dict() for serialization to json strings and dictionaries.

        .json(): Serialize to a JSON object.
        .dict(): Serialize to a dictionary.

    """

    valuations: List[Valuation]

    @property
    def dataframe(self) -> DataFrame:
        """Valuation Measures Table as a dataframe."""
        data = self.dict()
        dataframe = DataFrame.from_dict(data["valuations"])
        dataframe.set_index("date", inplace=True)
        dataframe.sort_index(inplace=True)
        return dataframe


class FinancialHighlights(Base):
    """Financial highlights section of a yahoo finance statistics page.

    Attributes:
        fiscal_year_ends (Date):
        most_recent_quarter_mrq (Date):

        profit_margin (float):
        operating_margin_ttm (float):

        return_on_assets_ttm (float):
        return_on_equity_ttm (float):

        revenue_ttm (int):
        revenue_per_share_ttm (float):
        quarterly_revenue_growth_yoy (float):
        gross_profit_ttm (int):
        ebitda (int):
        net_income_avi_to_common_ttm (int):
        diluted_eps_ttm (float):
        quarterly_earnings_growth_yoy (float):

        total_cash_mrq (int):
        total_cash_per_share_mrq (float):
        total_debt_mrq (int):
        total_debt_equity_mrq (float):
        current_ratio_mrq (float):
        book_value_per_share_mrq (float):

        levered_free_cash_flow_ttm (int):
        operating_cash_flow_ttm (int):

    Notes:
        This class inherits from the pydantic BaseModel which allows for the use
        of .json() and .dict() for serialization to json strings and dictionaries.

        .json(): Serialize to a JSON object.
        .dict(): Serialize to a dictionary.

    """

    fiscal_year_ends: Optional[Date]
    most_recent_quarter_mrq: Optional[Date]

    profit_margin: Optional[float]
    operating_margin_ttm: Optional[float]

    return_on_assets_ttm: Optional[float]
    return_on_equity_ttm: Optional[float]

    revenue_ttm: Optional[int]
    revenue_per_share_ttm: Optional[float]
    quarterly_revenue_growth_yoy: Optional[float]
    gross_profit_ttm: Optional[int]
    ebitda: Optional[int]
    net_income_avi_to_common_ttm: Optional[int]
    diluted_eps_ttm: Optional[float]
    quarterly_earnings_growth_yoy: Optional[float]

    total_cash_mrq: Optional[int]
    total_cash_per_share_mrq: Optional[float]
    total_debt_mrq: Optional[int]
    total_debt_equity_mrq: Optional[float]
    current_ratio_mrq: Optional[float]
    book_value_per_share_mrq: Optional[float]

    levered_free_cash_flow_ttm: Optional[int]
    operating_cash_flow_ttm: Optional[int]

    _clean_dates = cleaner("fiscal_year_ends", "most_recent_quarter_mrq")(
        CommonCleaners.clean_date
    )

    _clean_percentages = cleaner(
        "profit_margin",
        "operating_margin_ttm",
        "return_on_assets_ttm",
        "return_on_equity_ttm",
        "quarterly_revenue_growth_yoy",
        "quarterly_earnings_growth_yoy",
    )(CommonCleaners.clean_basic_percentage)

    _clean_common_values = cleaner(
        "book_value_per_share_mrq",
        "revenue_ttm",
        "revenue_per_share_ttm",
        "total_cash_mrq",
        "gross_profit_ttm",
        "ebitda",
        "net_income_avi_to_common_ttm",
        "diluted_eps_ttm",
        "total_cash_per_share_mrq",
        "total_debt_mrq",
        "total_debt_equity_mrq",
        "current_ratio_mrq",
        "levered_free_cash_flow_ttm",
        "operating_cash_flow_ttm",
    )(CommonCleaners.clean_common_values)


class TradingInformation(Base):
    """Trading information section of a yahoo finance statistics page.

    Attributes:
        beta_five_year_monthly (float):

        fifty_two_week_change (float):
        sp500_fifty_two_week_change (float):
        fifty_two_week_high (float):
        fifty_two_week_low (float):
        fifty_day_moving_average (float):
        two_hundred_day_moving_average (float):

        average_three_month_volume (int):
        average_ten_day_volume (int):
        shares_outstanding (int):
        float (int):
        percent_held_by_insiders (float):
        percent_held_by_institutions (float):

        shares_short (int):
        shares_short_date (Date):
        short_ratio (float):
        short_ratio_date (Date):
        short_percent_of_float (float):
        short_percent_of_float_date (Date):
        short_percent_of_shares_outstanding (float):
        short_percent_of_shares_outstanding_date (Date):
        shares_short_prior_month (int):
        shares_short_prior_month_date (Date):

        forward_annual_dividend_rate (float):
        forward_annual_dividend_yield (float):
        trailing_annual_dividend_rate (float):
        trailing_annual_dividend_yield (float):

        five_year_average_dividend_yield (float):

        payout_ratio (float):
        dividend_date (Date):
        exdividend_date (Date):
        last_split_factor (str):
        last_split_date (Date):

    Notes:
        This class inherits from the pydantic BaseModel which allows for the use
        of .json() and .dict() for serialization to json strings and dictionaries.

        .json(): Serialize to a JSON object.
        .dict(): Serialize to a dictionary.

    """

    beta_five_year_monthly: Optional[float]

    fifty_two_week_change: Optional[float] = Field(alias="fifty_twoweek_change_3")
    sp500_fifty_two_week_change: Optional[float] = Field(alias="sp500_fifty_twoweek_change_3")
    fifty_two_week_high: Optional[float] = Field(alias="fifty_two_week_high_3")
    fifty_two_week_low: Optional[float] = Field(alias="fifty_two_week_low_3")
    fifty_day_moving_average: Optional[float] = Field(alias="fifty_day_moving_average_3")
    two_hundred_day_moving_average: Optional[float] = Field(
        alias="two_hundred_day_moving_average_3"
    )

    average_three_month_volume: Optional[int] = Field(alias="avg_vol_three_month_3")
    average_ten_day_volume: Optional[int] = Field(alias="avg_vol_ten_day_3")
    shares_outstanding: Optional[int] = Field(alias="shares_outstanding_5")
    float: Optional[int]
    percent_held_by_insiders: Optional[float] = Field(alias="percent_held_by_insiders_1")
    percent_held_by_institutions: Optional[float] = Field(alias="percent_held_by_institutions_1")

    shares_short: Optional[int]
    shares_short_date: Optional[Date]
    short_ratio: Optional[float]
    short_ratio_date: Optional[Date]
    short_percent_of_float: Optional[float]
    short_percent_of_float_date: Optional[Date]
    short_percent_of_shares_outstanding: Optional[float]
    short_percent_of_shares_outstanding_date: Optional[Date]
    shares_short_prior_month: Optional[int]
    shares_short_prior_month_date: Optional[Date]

    forward_annual_dividend_rate: Optional[float] = Field(alias="forward_annual_dividend_rate_4")
    forward_annual_dividend_yield: Optional[float] = Field(alias="forward_annual_dividend_yield_4")
    trailing_annual_dividend_rate: Optional[float] = Field(alias="trailing_annual_dividend_rate_3")
    trailing_annual_dividend_yield: Optional[float] = Field(
        alias="trailing_annual_dividend_yield_3"
    )

    five_year_average_dividend_yield: Optional[float] = Field(
        alias="five_year_average_dividend_yield_4"
    )
    payout_ratio: Optional[float] = Field(alias="payout_ratio_4")
    dividend_date: Optional[Date] = Field(alias="dividend_date_3")
    exdividend_date: Optional[Date] = Field(alias="exdividend_date_4")
    last_split_factor: Optional[str] = Field(alias="last_split_factor_2")  # TODO: Not sure yet
    last_split_date: Optional[Date] = Field(alias="last_split_date_3")

    _clean_common_values = cleaner(
        "beta_five_year_monthly",
        "fifty_two_week_high",
        "fifty_two_week_low",
        "fifty_day_moving_average",
        "two_hundred_day_moving_average",
        "average_three_month_volume",
        "average_ten_day_volume",
        "shares_outstanding",
        "float",
        "shares_short",
        "short_ratio",
        "shares_short_prior_month",
        "forward_annual_dividend_rate",
        "trailing_annual_dividend_rate",
        "five_year_average_dividend_yield",
    )(CommonCleaners.clean_common_values)

    _clean_percentages = cleaner(
        "fifty_two_week_change",
        "sp500_fifty_two_week_change",
        "percent_held_by_insiders",
        "percent_held_by_institutions",
        "short_percent_of_float",
        "short_percent_of_shares_outstanding",
        "forward_annual_dividend_yield",
        "trailing_annual_dividend_yield",
        "payout_ratio",
    )(CommonCleaners.clean_basic_percentage)

    _clean_date = cleaner(
        "shares_short_date",
        "short_ratio_date",
        "short_percent_of_float_date",
        "short_percent_of_shares_outstanding_date",
        "shares_short_prior_month_date",
        "dividend_date",
        "exdividend_date",
        "last_split_date",
    )(CommonCleaners.clean_date)


def parse_valuation_table(
    html: HTML, period_type: PeriodType = PeriodType.QUARTERLY
) -> Optional[ValuationMeasuresTable]:
    """Parse and clean fields and rows of a valuation measures table HTML element.

    Args:
        html: Html element contatining valuation table data.
        period_type (PeriodType): The period to be parsed. Only quarterly is currently supported.

    Returns:
        ValuationMeasuresTable: If data is found.
        None: No data avaliable.
    """
    # IDEA: Parse the period type based on if it is a link or not.
    def clean_date(date_: str) -> str:
        """Clean field of a valuation table with date."""
        return date_.replace("Current", "").replace("As of Date:", "").strip()

    table_element = html.find(r"table.W\(100\%\).Bdcl\(c\).M\(0\).Whs\(n\).D\(itb\)", first=True)
    if table_element:

        table = pandas.read_html(table_element.html, index_col=0)
        table = table[0].transpose()
        table = table.replace(np.nan, "N/A", regex=True)

        valuations = []

        data = {}

        data["period_type"] = period_type
        for date_, row in table.iterrows():
            data["date"] = clean_date(date_)

            for field, value in row.items():
                field = field_cleaner(field)
                data[field] = value

            valuations.append(Valuation(**data))

        return ValuationMeasuresTable(valuations=valuations)

    return None


def parse_financial_highlights_table(html: HTML) -> Optional[FinancialHighlights]:
    """Parse and clean fields and rows of a financial highlights section of an HTML element."""
    table = html.find(r".Mb\(10px\).Pend\(20px\).smartphone_Pend\(0px\)", first=True)

    if table:
        table_data = table_cleaner(table)

        return FinancialHighlights(**table_data)

    return None


def parse_trading_information_table(html: HTML) -> Optional[TradingInformation]:
    """Parse and clean fields and rows of a trading information section of an HTML element."""
    table_element = html.find(r".Fl\(end\).W\(50\%\).smartphone_W\(100\%\)", first=True)

    if table_element:

        rows = [row.text.split("\n") for row in table_element.find("tr")]
        rows = list(filter(lambda row: len(row) == 2, rows))

        table_data = table_cleaner(html)

        if not table_data:
            table_data = {}

        for field, value in rows:
            if CommonCleaners.value_is_missing(value):
                continue

            if "Short" in field:
                field = field.replace("(prior month ", "prior month (")

                field_name, date_ = field.split("(")

                field_name = field_cleaner(field_name)
                date_ = date_.replace(") 4", "")

                table_data[field_name + "date"] = date_
                table_data[field_name.strip("_")] = value

        if table_data:
            return TradingInformation(**table_data)

    return None


class StatisticsPage(Base):
    """Represents all data you can find on a yahoo finance statistics page.

    Attributes:
        symbol (st): Ticker Symbol
        quote (Quote): Quote data from the quote header section.
        valuation_measures (ValuationMeasuresTable): Valuation Measures Table section.
        financial_highlights (FinancialHighlights): Financial Highlights section.
        trading_information (TradingInformation): Trading Information section

    Notes:
        This class inherits from the pydantic BaseModel which allows for the use
        of .json() and .dict() for serialization to json strings and dictionaries.

        .json(): Serialize to a JSON object.
        .dict(): Serialize to a dictionary.

    """

    symbol: str
    quote: Quote
    valuation_measures: ValuationMeasuresTable
    financial_highlights: FinancialHighlights
    trading_information: TradingInformation


class StatisticsPageGroup(Base):
    """Multiple Statistics Pages Group together.

    Attributes:
        pages: Multiple StatisticsPage objects. A page per symbol requested.

    Notes:
        This class inherits from the pydantic BaseModel which allows for the use
        of .json() and .dict() for serialization to json strings and dictionaries.

        .json(): Serialize to a JSON object.
        .dict(): Serialize to a dictionary.

    """

    pages: List[StatisticsPage]

    @property
    def dataframe(self: "StatisticsPageGroup") -> DataFrame:
        """Return a dataframe of multiple statistics pages."""
        data = []
        for page in self.pages:
            chain_map = ChainMap(
                page.quote.dict(),
                page.financial_highlights.dict(),
                page.trading_information.dict(),
            )
            chain_map["symbol"] = page.symbol
            data.append(chain_map)

        dataframe = DataFrame.from_dict(data)
        dataframe.set_index("symbol", inplace=True)
        dataframe.sort_index(inplace=True)
        return dataframe


class StatisticsPageNotFound(AttributeError):
    """Raised when statistics page data is not found."""


def get_statistics_page(
    symbol: str,
    use_fuzzy_search: bool = True,
    page_not_found_ok: bool = False,
    **kwargs,  # noqa: ANN003
) -> Optional[StatisticsPage]:
    """Get statistics page data.

    Args:
        symbol (str): Ticker symbol
        use_fuzzy_search (bool): If True does a symbol lookup validation prior
            to requesting options page data.
        page_not_found_ok (bool): If True Returns None when page is not found.
        **kwargs: requestor kwargs (session, proxies, and timeout)

    Returns:
        StatisticsPage: When data is found.
        None: No data is found and page_not_found_ok is True.

    Raises:
        StatisticsPageNotFound: When a page is not found and the page_not_found_ok arg is false.
    """
    if use_fuzzy_search:
        fuzzy_response = fuzzy_search(symbol, first_ticker=True, **kwargs)

        if fuzzy_response:
            symbol = fuzzy_response.symbol

    url = f"https://finance.yahoo.com/quote/{symbol}/key-statistics?p={symbol}"

    response = requestor(url)

    if response.ok:

        html = HTML(html=response.text)

        quote = parse_quote_header_info(html)
        valulation_measures = parse_valuation_table(html)
        financial_highlights = parse_financial_highlights_table(html)
        trading_information = parse_trading_information_table(html)

        if quote and valulation_measures and financial_highlights and trading_information:

            return StatisticsPage(
                symbol=symbol,
                quote=quote,
                valuation_measures=valulation_measures,
                financial_highlights=financial_highlights,
                trading_information=trading_information,
            )
    if page_not_found_ok:
        return None

    raise StatisticsPageNotFound(f"{symbol} statistics page not found.")
