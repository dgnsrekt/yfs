from yfs.lookup import fuzzy_search
from yfs.requestor import requestor
from yfs.cleaner import cleaner, field_cleaner, table_cleaner, CommonCleaners
from pydantic import BaseModel as Base
from pydantic import validator, Field, validate_arguments

from typing import Tuple, List, Dict, Optional, Union

import requests
from requests import Session
from requests_html import HTML

from collections import ChainMap

import pendulum
from pendulum.period import Period
from pendulum.date import Date
from pendulum.datetime import DateTime

import pandas
from pandas import DataFrame
from time import time

from pprint import pprint

from itertools import cycle

from enum import Enum

TICKERS = ["TSLA", "AAPL", "GOOGLE", "FCEL"]

symbol = "BYND"


class ContractExpiration(Base):
    symbol: str
    timestamp: str
    expiration_date: DateTime = Field(alias="timestamp")

    @validator("expiration_date", pre=True)
    def convert_to_datetime(cls, value):
        expiration_date = pendulum.from_timestamp(int(value), tz="UTC")
        return expiration_date

    def __lt__(self, other):
        if other.__class__ is self.__class__:
            return self.expiration_date < other.expiration_date


class ContractExpirationList(Base):
    expiration_list: List[ContractExpiration]

    @validator("expiration_list")
    def sort_dates(cls, values):
        return sorted(values)

    def filter_expirations_after(self, after: DateTime):
        filtered = list(filter(lambda exp: exp.expiration_date >= after, self.expiration_list))
        self.expiration_list = filtered

    def filter_expirations_before(self, before: DateTime):
        filtered = list(filter(lambda exp: exp.expiration_date <= before, self.expiration_list))
        self.expiration_list = filtered

    def filter_expirations_between(self, after: DateTime, before: DateTime):
        self.filter_expirations_after(after=after)
        self.filter_expirations_before(before=before)

    def filter_expirations_after_days(self, days: int):
        after = pendulum.now().add(days=days)
        self.filter_expirations_after(after=after)

    def filter_expirations_before_days(self, days: int):
        before = pendulum.now().add(days=days)
        self.filter_expirations_before(before=before)

    def filter_expirations_between_days(
        self, after_days: Optional[int] = None, before_days: Optional[int] = None
    ):
        if after_days:
            self.filter_expirations_after_days(days=after_days)
        if before_days:
            self.filter_expirations_before_days(days=before_days)

    def __len__(self):
        return len(self.expiration_list)

    def __iter__(self):
        return iter(self.expiration_list)

    def __add__(self, other):
        if self.__class__ == other.__class__:
            expiration_list = self.expiration_list + other.expiration_list
            return ContractExpirationList(expiration_list=expiration_list)


class OptionContractType(str, Enum):
    CALL = "call"
    PUT = "put"


class OptionContract(Base):
    symbol: str
    contract_type: OptionContractType
    timestamp: str
    expiration_date: DateTime  # already parsed from ContractExpiration
    in_the_money: bool

    contract_name: str
    # last_trade_date: Optional[DateTime]
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
    #     return pendulum.parse(value, strict=False)  # TODO: clean this up

    _clean_common_values = cleaner(
        "strike", "last_price", "bid", "ask", "volume", "open_interest"
    )(CommonCleaners.clean_common_values)

    _clean_percentages = cleaner("change", "percent_change", "implied_volatility")(
        CommonCleaners.clean_basic_percentage
    )

    class Config:
        use_enum_values = True


class OptionsChain(Base):
    symbol: str
    expiration_date: DateTime
    chain: List[OptionContract]

    @property
    def dataframe(self):
        data = self.dict()
        chain_data = data["chain"]
        dataframe = DataFrame.from_dict(chain_data)
        return dataframe

    @property
    def calls(self):
        call_chain = list(
            filter(lambda contract: contract.contract_type == OptionContractType.CALL, self.chain)
        )
        return OptionsChain(
            symbol=self.symbol, expiration_date=self.expiration_date, chain=call_chain
        )

    @property
    def puts(self):
        put_chain = list(
            filter(lambda contract: contract.contract_type == OptionContractType.PUT, self.chain)
        )
        return OptionsChain(
            symbol=self.symbol, expiration_date=self.expiration_date, chain=put_chain
        )

    def __len__(self):
        return len(self.chain)


class MutipleOptionChains(Base):
    option_chain_list: List[OptionsChain]
    contract_expiration_list: ContractExpirationList

    @property
    def dataframe(self):

        if len(self.option_chain_list) == 1:
            return self.option_chain_list[0].dataframe

        else:
            dataframes = []

            for option_chain in self.option_chain_list:
                dataframes.append(option_chain.dataframe)

            return pandas.concat(dataframes, ignore_index=True)

    @property
    def calls(self):
        calls = [chain.calls for chain in self]
        return MutipleOptionChains(
            option_chain_list=calls, contract_expiration_list=self.contract_expiration_list
        )

    @property
    def puts(self):
        puts = [chain.puts for chain in self]
        return MutipleOptionChains(
            option_chain_list=puts, contract_expiration_list=self.contract_expiration_list
        )

    def __len__(self):
        return len(self.option_chain_list)

    def __iter__(self):
        return iter(self.option_chain_list)

    def __add__(self, other):
        if self.__class__ == other.__class__:
            option_chain_list = self.option_chain_list + other.option_chain_list
            contract_expiration_list = (
                self.contract_expiration_list + other.contract_expiration_list
            )
            return MutipleOptionChains(
                option_chain_list=option_chain_list,
                contract_expiration_list=contract_expiration_list,
            )


def get_table_elements(html):
    calls_table = html.find("table.calls", first=True)
    puts_table = html.find("table.puts", first=True)
    return calls_table, puts_table


def parse_option_table(contract_expiration, contract_type, options_table):
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


def get_option_expirations(symbol: str, **kwargs):
    url = f"https://finance.yahoo.com/quote/{symbol}/options?p={symbol}"

    response = requests.get(url, **kwargs)

    if response.ok:

        html = HTML(html=response.text, url=url)

        elements = html.find("div.Fl\(start\).Pend\(18px\)", first=True)

        if elements:

            timestamps = [element.attrs["value"] for element in elements.find("option")]

            expiration_list = [
                ContractExpiration(symbol=symbol, timestamp=timestamp) for timestamp in timestamps
            ]

            return ContractExpirationList(expiration_list=expiration_list)

    return None


def get_options_page(
    symbol: str,
    after_days: int = None,
    before_days: int = None,
    first_chain: bool = False,
    use_fuzzy_search: bool = True,
    page_not_found_ok: bool = False,
    **kwargs,
):

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

            calls = parse_option_table(expiration, "call", calls_table)
            puts = parse_option_table(expiration, "put", puts_table)

            chain = calls + puts

            option_chain = OptionsChain(
                symbol=symbol, expiration_date=expiration.expiration_date, chain=chain
            )

            if first_chain:
                return option_chain
            else:
                mutiple_option_chains.append(option_chain)

    else:
        if len(mutiple_option_chains) > 0:

            return MutipleOptionChains(
                option_chain_list=mutiple_option_chains, contract_expiration_list=expirations_list
            )

    return None
