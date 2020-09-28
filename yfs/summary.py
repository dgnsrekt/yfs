from collections import ChainMap
from typing import List, Optional

import enlighten
from pandas import DataFrame
import pendulum
from pendulum.date import Date
from pydantic import BaseModel as Base
from pydantic import Field
from pydantic import validator as clean
from requests_html import HTML

from .cleaner import cleaner, field_cleaner, table_cleaner, CommonCleaners
from .quote import parse_quote_header_info, Quote
from .requestor import requestor
from .lookup import fuzzy_search


class SummaryPage(Base):
    # Model representing the yahoo finance summary page.
    symbol: str
    name: str  # from quote

    quote: Quote

    open: Optional[float]
    high: Optional[float] = Field(alias="days_range")
    low: Optional[float] = Field(alias="days_range")
    close: Optional[float]  # pre-cleaned from quote

    change: Optional[float]  # pre-cleaned from quote
    percent_change: Optional[float]  # pre-cleaned from quote

    previous_close: Optional[float]

    bid_price: Optional[float] = Field(alias="bid")
    bid_size: Optional[int] = Field(alias="bid")

    ask_price: Optional[float] = Field(alias="ask")
    ask_size: Optional[int] = Field(alias="ask")

    fifty_two_week_low: Optional[float] = Field(alias="fifty_two_week_range")
    fifty_two_week_high: Optional[float] = Field(alias="fifty_two_week_range")

    volume: Optional[int]
    average_volume: Optional[int] = Field(alias="avg_volume")

    market_cap: Optional[int]

    beta_five_year_monthly: Optional[float]
    pe_ratio_ttm: Optional[float]
    eps_ttm: Optional[float]

    earnings_date: Optional[Date]

    forward_dividend_yield: Optional[float]
    forward_dividend_yield_percentage: Optional[float] = Field(alias="forward_dividend_yield")
    exdividend_date: Optional[Date]

    one_year_target_est: Optional[float]

    _clean_symbol = cleaner("symbol")(CommonCleaners.clean_symbol)

    _clean_highs = cleaner("high", "fifty_two_week_high")(
        CommonCleaners.clean_first_value_split_by_dash
    )
    _clean_lows = cleaner("low", "fifty_two_week_low")(
        CommonCleaners.clean_second_value_split_by_dash
    )
    _clean_date = cleaner("earnings_date", "exdividend_date")(CommonCleaners.clean_date)

    _clean_common_values = cleaner(
        "open",
        "previous_close",
        "market_cap",
        "volume",
        "average_volume",
        "pe_ratio_ttm",
        "beta_five_year_monthly",
        "eps_ttm",
        "one_year_target_est",
    )(CommonCleaners.clean_common_values)

    _clean_forward_dividend_yield = cleaner("forward_dividend_yield")(
        CommonCleaners.clean_first_value_split_by_space
    )

    _clean_forward_dividend_yield_percentage = cleaner("forward_dividend_yield_percentage")(
        CommonCleaners.clean_second_value_split_by_space
    )

    _clean_bid_ask_price = cleaner("bid_price", "ask_price")(
        CommonCleaners.clean_first_value_split_by_x
    )

    _clean_bid_ask_volume = cleaner("bid_size", "ask_size")(
        CommonCleaners.clean_second_value_split_by_x
    )

    def __lt__(self, other):
        if other.__class__ is self.__class__:
            return self.symbol < other.symbol


class SummaryPageGroup(Base):
    data: List[SummaryPage]

    @property
    def symbols(self):
        return [symbol.symbol for symbol in self]

    def sorted(self):
        return SummaryPageGroup(data=sorted(self.data))

    @property
    def dataframe(self, sorted=True):
        data = self.dict()
        dataframe = DataFrame.from_dict(data["data"])
        dataframe.set_index("symbol", inplace=True)
        dataframe.drop("quote", axis=1, inplace=True)

        if sorted:
            dataframe.sort_index(inplace=True)
        return dataframe  # TODO: none or nan

    def __iter__(self):
        return iter(self.data)

    def __len__(self):
        return len(self.data)


def parse_summary_table(html: HTML):
    quote_summary = html.find("div#quote-summary", first=True)

    if quote_summary:
        return table_cleaner(quote_summary)
    else:
        return None


class SummaryPageNotFound(AttributeError):
    pass


def get_summary_page(
    symbol: str,
    use_fuzzy_search=True,
    page_not_found_ok=False,
    **kwargs,  # fuzzy search exchange_type, asset_type, session, proxies, timeout
):

    if use_fuzzy_search:
        fuzzy_response = fuzzy_search(symbol, first_ticker=True, **kwargs)

        if fuzzy_response:
            symbol = fuzzy_response.symbol

    url = f"https://finance.yahoo.com/quote/{symbol}?p={symbol}"

    response = requestor(url, **kwargs)

    if response.ok:

        html = HTML(html=response.text, url=url)

        quote_data = parse_quote_header_info(html)

        summary_page_data = parse_summary_table(html)

        if quote_data and summary_page_data:
            data = ChainMap(quote_data.dict(), summary_page_data)
            data["symbol"] = symbol
            data["quote"] = quote_data

            return SummaryPage(**data)

    if page_not_found_ok:
        return None
    else:
        raise SummaryPageNotFound(f"{symbol} summary page not found.")


def _download_summary_pages_without_threads(
    symbols: List[str],
    use_fuzzy_search,
    page_not_found_ok,
    progress_bar,
    **kwargs,  # fuzzy search exchange_type, asset_type, session, proxies, timeout
):

    data = []

    if use_fuzzy_search:
        valid_symbols = []

        if progress_bar:
            pbar = enlighten.Counter(
                total=len(symbols), desc="Validating symbols...", unit="symbols"
            )

        for symbol in symbols:
            result = fuzzy_search(
                symbol,
                first_ticker=True,
                **kwargs,  # fuzzy search exchange_type, asset_type, session, proxies, timeout
            )

            valid_symbols.append(result)

            if progress_bar:
                pbar.update()

        valid_symbols = filter(lambda s: s is not None, valid_symbols)
        symbols = list(set([s.symbol for s in valid_symbols]))

    if progress_bar:
        pbar = enlighten.Counter(
            total=len(symbols), desc="Downloading Summary Data...", unit="symbols"
        )

    for symbol in symbols:
        results = get_summary_page(
            symbol,
            use_fuzzy_search=False,
            page_not_found_ok=page_not_found_ok,
            **kwargs,  # fuzzy search exchange_type, asset_type, session, proxies, timeout
        )

        if results:
            data.append(results)

        if progress_bar:
            pbar.update()

    if data:
        return SummaryPageGroup(data=data)

    else:
        return None


def _download_summary_pages_with_threads(
    symbols: List[str],
    use_fuzzy_search,
    page_not_found_ok,
    thread_count,
    progress_bar,
    **kwargs,  # fuzzy_search: exchange_type, asset_type, requestor: session, proxies, timeout
):
    data = []

    from concurrent.futures import as_completed, ThreadPoolExecutor

    if use_fuzzy_search:
        valid_symbols = []

        with ThreadPoolExecutor(max_workers=thread_count) as executor:
            futures = [
                executor.submit(
                    fuzzy_search,
                    symbol,
                    first_ticker=True,
                    **kwargs,  # fuzzy_search: exchange_type, asset_type,
                    # kwargs also for requestor: session, proxies, timeout
                )
                for symbol in symbols
            ]

            if progress_bar:
                pbar = enlighten.Counter(
                    total=len(futures), desc="Validating symbols...", unit="symbols"
                )

            for future in as_completed(futures):
                valid_symbols.append(future.result())

                if progress_bar:
                    pbar.update()

        valid_symbols = filter(lambda s: s is not None, valid_symbols)
        symbols = list(set([s.symbol for s in valid_symbols]))

    with ThreadPoolExecutor(max_workers=thread_count) as executor:
        futures = [
            executor.submit(
                get_summary_page,
                symbol,
                use_fuzzy_search=False,
                page_not_found_ok=page_not_found_ok,
                **kwargs,  # fuzzy_search: exchange_type, asset_type,
                # kwargs also for requestor: session, proxies, timeout
            )
            for symbol in symbols
        ]

        if progress_bar:
            pbar = enlighten.Counter(
                total=len(futures), desc="Downloading Summary Data...", unit="symbols"
            )

        for future in as_completed(futures):
            results = future.result()

            if results:
                data.append(results)

            if progress_bar:
                pbar.update()

    if data:
        return SummaryPageGroup(data=data)

    else:
        return None


def get_multiple_summary_pages(
    symbols: List[str],
    use_fuzzy_search=True,
    page_not_found_ok=False,
    with_threads=False,
    thread_count=5,
    progress_bar=True,
    **kwargs,  # fuzzy_search: exchange_type, asset_type, requestor: session, proxies, timeout
):
    symbols = list(set(symbols))

    if with_threads:
        return _download_summary_pages_with_threads(
            symbols,
            use_fuzzy_search=use_fuzzy_search,
            page_not_found_ok=page_not_found_ok,
            thread_count=thread_count,
            progress_bar=progress_bar,
            **kwargs,  # fuzzy search exchange_type, asset_type
        )
    else:
        return _download_summary_pages_without_threads(
            symbols,
            use_fuzzy_search=use_fuzzy_search,
            page_not_found_ok=page_not_found_ok,
            progress_bar=progress_bar,
            **kwargs,  # fuzzy search exchange_type, asset_type
        )
