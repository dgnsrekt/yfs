from .cleaner import cleaner, field_cleaner, table_cleaner, CommonCleaners
from .requestor import requestor
from .quote import parse_quote_header_info, Quote
from .lookup import fuzzy_search

from pydantic import BaseModel as Base
from pydantic import Field

import pendulum
from pendulum.date import Date
from requests_html import HTML
import pandas
from pandas import DataFrame
from pandas import Series
import numpy as np

from typing import List, Optional

from enum import Enum

from collections import ChainMap


class PeriodType(str, Enum):
    ANNUALY = "Annual"
    QUARTERLY = "Quarterly"
    MONTHLY = "Monthly"


class Valuation(Base):
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
        use_enum_values = True


class ValuationMeasuresTable(Base):
    valuations: List[Valuation]

    @property
    def dataframe(self):
        data = self.dict()
        dataframe = DataFrame.from_dict(data["valuations"])
        dataframe.set_index("date", inplace=True)
        dataframe.sort_index(inplace=True)
        return dataframe


class FinancialHighlights(Base):
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


def parse_valuation_table(html: HTML, period_type: PeriodType = PeriodType.QUARTERLY):
    # IDEA: Parse the period type based on if it is a link or not.
    def clean_date(date_):
        return date_.replace("Current", "").replace("As of Date:", "").strip()

    table_element = html.find("table.W\(100\%\).Bdcl\(c\).M\(0\).Whs\(n\).D\(itb\)", first=True)
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
    else:
        return None


def parse_financial_highlights_table(html):
    table = html.find(".Mb\(10px\).Pend\(20px\).smartphone_Pend\(0px\)", first=True)

    if table:
        table_data = table_cleaner(table)

        return FinancialHighlights(**table_data)

    else:
        return None


def parse_trading_information_table(html):
    table_element = html.find(".Fl\(end\).W\(50\%\).smartphone_W\(100\%\)", first=True)

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
    symbol: str
    quote: Quote
    valuation_measures: ValuationMeasuresTable
    financial_highlights: FinancialHighlights
    trading_information: TradingInformation


class StatisticsPageGroup(Base):
    pages: List[StatisticsPage]

    @property
    def dataframe(self):
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
    pass


def get_statistics_page(symbol: str, use_fuzzy_search=True, page_not_found_ok=False, **kwargs):
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

    else:
        raise StatisticsPageNotFound(f"{symbol} statistics page not found.")
