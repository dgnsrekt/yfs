"""Contains the classes and functions for scraping a yahoo finance option page."""

from enum import Enum
from itertools import cycle
from typing import Iterable, List, Optional, Tuple, Union

import pandas
from pandas import DataFrame
import pendulum
from pendulum.datetime import DateTime
from pydantic import BaseModel as Base
from pydantic import Field, validator
from requests_html import HTML

from .cleaner import cleaner, CommonCleaners, field_cleaner
from .lookup import fuzzy_search
from .requestor import requestor


class ContractExpiration(Base):
    """Contract Expiration.

    Attributes:
        symbol (str): Ticker symbol.
        timestamp (str): Timestamp of expiration date.
        expiration_date (DateTime): Datetime of expiration date.

    Notes:
        This class inherits from the pydantic BaseModel which allows for the use
        of .json() and .dict() for serialization to json strings and dictionaries.

        .json(): Serialize to a JSON object.
        .dict(): Serialize to a dictionary.
    """

    symbol: str
    timestamp: str
    expiration_date: DateTime = Field(alias="timestamp")

    @validator("expiration_date", pre=True)
    def convert_to_datetime(cls, value: str) -> DateTime:  # pylint: disable=E0213,R0201
        """Convert expiration timestamp to datetime."""
        expiration_date = pendulum.from_timestamp(int(value), tz="UTC")
        return expiration_date

    def __lt__(self, other: "ContractExpiration") -> Optional["ContractExpiration"]:
        """Compare expiration_dates for sorting."""
        if other.__class__ is self.__class__:
            return self.expiration_date < other.expiration_date
        return None


class ContractExpirationList(Base):
    """Contains Multiple Expirations.

    Attributes:
        expiration_list (List[ContractExpiration]): multiple expirations.

    Notes:
        This class inherits from the pydantic BaseModel which allows for the use
        of .json() and .dict() for serialization to json strings and dictionaries.

        .json(): Serialize to a JSON object.
        .dict(): Serialize to a dictionary.

    """

    expiration_list: List[ContractExpiration]

    @validator("expiration_list")
    def sort_dates(  # pylint: disable=E0213,R0201
        cls, values: List[ContractExpiration]
    ) -> List[ContractExpiration]:
        """Sort expiration_list by date."""
        return sorted(values)

    def filter_expirations_after(self, after: DateTime) -> None:
        """Filter out any expiration dates prior to the after date.

        Args:
            after (DateTime): datetime to filter.

        Example:
            |Input                      | Args         |Output            |
            |---------------------------|--------------|------------------|
            |[01JAN19, 01FEB19, 01MAR19]|after: 15JAN19|[01FEB19, 01MAR19]|
        """
        filtered = list(filter(lambda exp: exp.expiration_date >= after, self.expiration_list))
        self.expiration_list = filtered

    def filter_expirations_before(self, before: DateTime) -> None:
        """Filter out any expiration dates post the before date.

        Args:
            before (DateTime): datetime to filter.

        Example:
            |Input                      | Args          |Output   |
            |---------------------------|---------------|---------|
            |[01JAN19, 01FEB19, 01MAR19]|before: 15JAN19|[01JAN19]|

        """
        filtered = list(filter(lambda exp: exp.expiration_date <= before, self.expiration_list))
        self.expiration_list = filtered

    def filter_expirations_between(self, after: DateTime, before: DateTime) -> None:
        """Filter dates outside of a after and before range.

        Args:
            after (DateTime): datetime to filter.
            before (DateTime): datetime to filter.

        Example:
            |Input                      | Args                         |Output            |
            |---------------------------|------------------------------|------------------|
            |[01JAN19, 01FEB19, 01MAR19]|after: 15JAN19,before: 15JAN19|[01FEB19, 01MAR19]|
        """
        self.filter_expirations_after(after=after)
        self.filter_expirations_before(before=before)

    def filter_expirations_after_days(self, days: int) -> None:
        """Filter expirations only allowing expirations after n days.

        Args:
            days (int): Number of days to start filtering from. All expirations
                which expire prior to the days will be filtered out.
        """
        after = pendulum.now().add(days=days)
        self.filter_expirations_after(after=after)

    def filter_expirations_before_days(self, days: int) -> None:
        """Filter expiration only allowing expirations before n days.

        Args:
            days (int): Number of days to start filtering from. All expirations
                which expire post days will be filtered out.
        """
        before = pendulum.now().add(days=days)
        self.filter_expirations_before(before=before)

    def filter_expirations_between_days(
        self, after_days: Optional[int] = None, before_days: Optional[int] = None
    ) -> None:
        """Filter expiration only allowing expirations between a range of days.

        Args:
            after_days (int): Number of days to start filtering from. All expirations
                which expire prior to the days will be filtered out.
            before_days (int): Number of days to start filtering from. All expirations
                which expire post days will be filtered out.
        """
        if after_days:
            self.filter_expirations_after_days(days=after_days)

        if before_days:
            self.filter_expirations_before_days(days=before_days)

    def __len__(self) -> int:
        """Length of the expiration_list."""
        return len(self.expiration_list)

    def __iter__(self) -> Iterable:
        """Iterate over the expirations_list."""
        return iter(self.expiration_list)

    def __add__(self, other: "ContractExpirationList") -> Optional["ContractExpirationList"]:
        """Combine two ContractExpirationLists using the + operator."""
        if self.__class__ == other.__class__:
            expiration_list = self.expiration_list + other.expiration_list
            return ContractExpirationList(expiration_list=expiration_list)
        return None


class OptionContractType(str, Enum):
    """Enum for option contract types."""

    CALL = "call"
    PUT = "put"


class OptionContract(Base):
    """Represents an Option Contract.

    Attributes:
        symbol (str): Ticker symbol.
        contract_type (OptionContractType): Call or Put type.

        timestamp (str): Raw timestamp scraped from yahoo finance. This string is left
            untouched to make sure there is no issues when building a URL.
        expiration_date (DateTime): Converted from the timestamp. This allows allows
            sorting and filtering.
        in_the_money (bool): True if strike price is ITM else False.

        contract_name (str): Contract Name.
        last_trade_date (DateTime): Date of last trade.
        strike (float): Contracts strike price.
        last_price (float): Last price of a transaction between a contract buyer and a seller.

        bid (float): Last bid price.
        ask (float): Last ask price.

        change (float): Price change in dollars.
        percent_change (float): Price change in percentage.
        volume (int): Volume.
        open_interest (int): Number of contracts opened.
        implied_volatility (float): Contract IV.

    Notes:
        This class inherits from the pydantic BaseModel which allows for the use
        of .json() and .dict() for serialization to json strings and dictionaries.

        .json(): Serialize to a JSON object.
        .dict(): Serialize to a dictionary.
    """

    symbol: str
    contract_type: OptionContractType
    timestamp: str
    expiration_date: DateTime  # already parsed from ContractExpiration
    in_the_money: bool

    contract_name: str
    # last_trade_date: Optional[DateTime] #TODO: fix validator
    strike: Optional[float]
    last_price: Optional[float]

    bid: Optional[float]
    ask: Optional[float]

    change: Optional[float]
    percent_change: Optional[float]
    volume: Optional[int]
    open_interest: Optional[int]
    implied_volatility: Optional[float]

    # @cleaner("last_trade_date")
    # def clean_last_trade_date(cls, value):
    #     return pendulum.parse(value, strict=False)

    _clean_common_values = cleaner(
        "strike", "last_price", "bid", "ask", "volume", "open_interest"
    )(CommonCleaners.clean_common_values)

    _clean_percentages = cleaner("change", "percent_change", "implied_volatility")(
        CommonCleaners.clean_basic_percentage
    )

    class Config:  # noqa: D106 pylint: disable=C0115
        use_enum_values = True


class OptionsChain(Base):
    """Chain of option contracts with the same expiration date.

    Attributes:
        symbol (str): Company symbol.
        expiration_date (DateTime): Contracts expiration date.
        chain (List[OptionContract]): List of OptionContracts.

    Notes:
        This class inherits from the pydantic BaseModel which allows for the use
        of .json() and .dict() for serialization to json strings and dictionaries.

        .json(): Serialize to a JSON object.
        .dict(): Serialize to a dictionary.
    """

    symbol: str
    expiration_date: DateTime
    chain: List[OptionContract]

    @property
    def dataframe(self) -> DataFrame:
        """Return a dataframe of the option chain."""
        data = self.dict()
        chain_data = data["chain"]
        dataframe = DataFrame.from_dict(chain_data)
        return dataframe

    @property
    def calls(self) -> "OptionsChain":
        """Return a OptionChain with only call contracts."""
        call_chain = list(
            filter(lambda contract: contract.contract_type == OptionContractType.CALL, self.chain)
        )
        return OptionsChain(
            symbol=self.symbol, expiration_date=self.expiration_date, chain=call_chain
        )

    @property
    def puts(self) -> "OptionsChain":
        """Return a OptionChain with only put contracts."""
        put_chain = list(
            filter(lambda contract: contract.contract_type == OptionContractType.PUT, self.chain)
        )
        return OptionsChain(
            symbol=self.symbol, expiration_date=self.expiration_date, chain=put_chain
        )

    def __len__(self) -> int:
        """Return the number of OptionContracts in the OptionChain."""
        return len(self.chain)


class MultipleOptionChains(Base):
    """Multiple Option Chains with multiple expiration dates.

    Attributes:
        option_chain_list (List[OptionsChain]): List of option chains.
        contract_expiration_list (ContractExpirationList): List of expirations.

    Notes:
        This class inherits from the pydantic BaseModel which allows for the use
        of .json() and .dict() for serialization to json strings and dictionaries.

        .json(): Serialize to a JSON object.
        .dict(): Serialize to a dictionary.
    """

    option_chain_list: List[OptionsChain]
    contract_expiration_list: ContractExpirationList

    @property
    def dataframe(self) -> DataFrame:
        """Return a dataframe of multiple option chains."""
        if len(self.option_chain_list) == 1:
            return self.option_chain_list[0].dataframe

        dataframes = []

        for option_chain in self.option_chain_list:
            dataframes.append(option_chain.dataframe)

        return pandas.concat(dataframes, ignore_index=True)

    @property
    def calls(self) -> "MultipleOptionChains":
        """Return a MultipleOptionChains object with only call contracts."""
        calls = [chain.calls for chain in self]
        return MultipleOptionChains(
            option_chain_list=calls, contract_expiration_list=self.contract_expiration_list
        )

    @property
    def puts(self) -> "MultipleOptionChains":
        """Return a MultipleOptionChains object with only put contracts."""
        puts = [chain.puts for chain in self]
        return MultipleOptionChains(
            option_chain_list=puts, contract_expiration_list=self.contract_expiration_list
        )

    def __len__(self) -> int:
        """Return the number of option chains."""
        return len(self.option_chain_list)

    def __iter__(self) -> Iterable:
        """Iterate over option chain list."""
        return iter(self.option_chain_list)

    def __add__(self, other: "MultipleOptionChains") -> Optional["MultipleOptionChains"]:
        """Concatenate MultipleOptionChains."""
        if self.__class__ == other.__class__:
            option_chain_list = self.option_chain_list + other.option_chain_list
            contract_expiration_list = (
                self.contract_expiration_list + other.contract_expiration_list
            )
            return MultipleOptionChains(
                option_chain_list=option_chain_list,
                contract_expiration_list=contract_expiration_list,
            )
        return None  # NOTE: Maybe Should Raise here


def get_table_elements(html: HTML) -> Tuple[Optional[HTML], Optional[HTML]]:
    """Parse call and put HTML table elements.

    Args:
        html (HTML): HTML element with call and put data.

    Returns:
        Tuple of found call and put html elements.
    """
    calls_table = html.find("table.calls", first=True)
    puts_table = html.find("table.puts", first=True)
    return calls_table, puts_table


def parse_option_table(
    contract_expiration: ContractExpiration, contract_type: OptionContractType, options_table: HTML
) -> List[OptionContract]:
    """Parse and clean fields and rows of a options table HTML element.

    Args:
        contract_expiration (ContractExpiration): Used to pass ContractExpiration data
            to the returned OptionContract object.
        contract_type (OptionContractType): Call or Put
        options_table (HTML): HTML element with raw options table data.

    Returns:
        A list of OptionContracts parsed from the html options_table.
    """
    head = options_table.find("thead", first=True)
    body = options_table.find("tbody", first=True)

    headers = cycle(head.text.split("\n"))

    contracts = []

    for row in body.find("tr"):
        data = contract_expiration.dict()
        data["contract_type"] = contract_type

        if "in-the-money" in row.attrs["class"]:
            data["in_the_money"] = True
        else:
            data["in_the_money"] = False

        for value in row.text.split("\n"):
            column_name = field_cleaner(next(headers))
            data[column_name] = value

        contracts.append(OptionContract(**data))

    return contracts


def get_option_expirations(
    symbol: str, **kwargs  # noqa: ANN003
) -> Optional[ContractExpirationList]:
    """Get and parse option expiration data for the selected symbol.

    Args:
        symbol (str): Ticker symbol.
        kwargs: Pass (session, proxies, and timeout) to the requestor function.

    Returns:
        ContractExpirationList
    """
    url = f"https://finance.yahoo.com/quote/{symbol}/options?p={symbol}"

    response = requestor(url, **kwargs)

    if response.ok:

        html = HTML(html=response.text, url=url)

        elements = html.find(r"div.Fl\(start\).Pend\(18px\)", first=True)

        if elements:

            timestamps = [element.attrs["value"] for element in elements.find("option")]

            expiration_list = [
                ContractExpiration(symbol=symbol, timestamp=timestamp) for timestamp in timestamps
            ]

            return ContractExpirationList(expiration_list=expiration_list)

    return None


class OptionPageNotFound(AttributeError):
    """Raised when options page data is not found."""


def get_options_page(  # pylint: disable=R0913, R0914
    symbol: str,
    after_days: int = None,
    before_days: int = None,
    first_chain: bool = False,
    use_fuzzy_search: bool = True,
    page_not_found_ok: bool = False,
    **kwargs,  # noqa: ANN003
) -> Optional[Union[OptionsChain, MultipleOptionChains]]:
    """Get options data from yahoo finance options page.

    Args:
        symbol (str): Ticker symbol.
        after_days (int): Number of days to start filtering from. All expirations
            which expire prior to the days will be filtered out.
        before_days (int): Number of days to start filtering from. All expirations
            which expire post days will be filtered out.
        first_chain (bool): If True returns first chain. Else returns all found chains
            within search range.
        use_fuzzy_search (bool): If True, does a symbol lookup validation prior
            to requesting options page data.
        page_not_found_ok (bool): If True, returns None when page is not found.
        **kwargs: Pass (session, proxies, and timeout) to the requestor function.

    Returns:
        OptionsChain: If first_chain is set to True the first found OptionsChain
            within the after_days and before_days range is returned.
            This is all option contracts from a single expiration and symbol.
        MultipleOptionChains: If first_chain is set to False all OptionsChains within
            the after_days and before_days range are returned. This can have
            multiple expirations. Even if one expiration date is found
            the MultipleOptionChains object is returned.
        None: If no contracts are found and page_not_found_ok is True.

    Raises:
        OptionPageNotFound: If page_not_found_ok is False and the Options page is not found.

    """
    if use_fuzzy_search:
        fuzzy_response = fuzzy_search(symbol, first_ticker=True, **kwargs)

        if fuzzy_response:
            symbol = fuzzy_response.symbol

    expirations_list = get_option_expirations(symbol, **kwargs)

    if expirations_list is None:
        return None

    if after_days or before_days:
        expirations_list.filter_expirations_between_days(
            after_days=after_days, before_days=before_days
        )

    mutiple_option_chains = []

    for expiration in expirations_list:
        timestamp = expiration.timestamp
        symbol = expiration.symbol

        url = f"https://finance.yahoo.com/quote/{symbol}/options?date={timestamp}&p={symbol}"

        response = requestor(url, **kwargs)

        if response.ok:

            html = HTML(html=response.text, url=url)

            calls_table, puts_table = get_table_elements(html)

            if calls_table is None or puts_table is None:
                continue

            calls = parse_option_table(expiration, "call", calls_table)
            puts = parse_option_table(expiration, "put", puts_table)

            chain = calls + puts

            option_chain = OptionsChain(
                symbol=symbol, expiration_date=expiration.expiration_date, chain=chain
            )

            if first_chain:
                return option_chain

            mutiple_option_chains.append(option_chain)

    if len(mutiple_option_chains) > 0:

        return MultipleOptionChains(
            option_chain_list=mutiple_option_chains, contract_expiration_list=expirations_list
        )

    if page_not_found_ok:
        return None

    raise OptionPageNotFound(f"{symbol} options pages is not found.")
