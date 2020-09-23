from pydantic import BaseModel as Base
from pydantic import validator, Field, ValidationError, PydanticValueError
from typing import List, Optional, Union
import requests
from requests_html import HTML
from pprint import pprint
from enum import Enum

DEBUG_MODE = True


class ExchangeNotFoundError(PydanticValueError):
    code = "not_a_valid_exchange"
    msg_template = "Found a missing exchange: {invalid_exchange}"


class AssetTypeNotFoundError(PydanticValueError):
    code = "not_a_valid_asset_type"
    msg_template = "Found a missing asset: {invalid_asset_type}"


class UnitedStatesExchanges(str, Enum):
    CBOE = "Chicago Board Options Exchange"
    CBOT = "Chicago Board of Trade"
    CME = "Chicago Mercantile Exchange"
    DOW = "Dow Jones"
    NASDAQ = "NASDAQ"
    NASDAQ_GIDS = "NASDAQ GIDS"
    NY_MERCANTIEL = "NY Mercantile"
    NYCE = "New York Commodity Exchange"
    NYBOT = "New York Board of Trade"
    NYSE = "NYSE"
    NSE = "NSE"
    NYSE_MKT = "NYSE MKT"
    NYSE_ARCA = "NYSEArca"
    OTC = "OTC Markets"
    OTC_BB = "OTC BB"


class ForeignExchanges(str, Enum):
    BUENOS_AIRES = "Buenos Aires"
    SAO_PAOLO = "Sao Paolo"
    MEXICO = "Mexico"
    MILAN = "Milan"
    VIENNA = "Vienna"
    SANTIAGO = "Santiago Stock Exchange"
    DUSSELDORF = "Dusseldorf Stock Exchange"
    FRANKFURT = "Frankfurt"
    MUNICH = "Munich"
    BERLIN = "Berlin"
    HAMBURG = "Hamburg"
    IRISH = "Irish"
    LONDON = "London"
    FTSE_GLOBAL_INDEX = "FTSEGlobal Index"
    LONDON_INTERNATIONAL = "International Orderbook - London"
    EURONEXT = "Euronext"
    JOHANNESBURG = "Johannesburg Stock Exchange"
    STUTTGART = "Stuttgart"
    TEL_AVIV = "Tel Aviv"
    PARIS = "Paris"
    JAKARTA = "Jakarta"
    AUSTRALIAN = "Australian"
    KUALA_LUMPUR = "Kuala Lumpur Stock Exchange"
    HONG_KONG = "Hong Kong"
    LISBON = "Lisbon Stock Exchange"
    TORONTO = "Toronto"
    AMSTERDAM = "Amsterdam"
    SINGAPORE = "Singapore"
    COLOMBO = "Colombo Stock Exchange"
    SWISS = "Swiss"
    SHENZHEN = "Shenzhen"
    TAIWAN = "Taiwan"
    MADRID = "Madrid Stock Exchange CATS"
    STOCKHOLM = "Stockholm"
    TOKYO = "Tokyo Stock Exchange"
    BOMBAY = "Bombay"
    SHANGHAI = "Shanghai"
    ZURICH = "Zurich Stock Exchange"
    SAUDI = "Saudi Stock Exchange"
    KOREA = "Korea"
    KOSDAQ = "KOSDAQ"
    NEW_ZEALAND = "New Zealand"
    PRAGUE = "Prague Stock Exchange"
    BRUSSELS = "Brussels Stock Exchange"
    HANOVER = "Hanover"
    COPENHAGEN = "Copenhagen"
    CAIRO = "Cairo Stock Exchange"
    ATHENS = "Athens"


class OtherExchanges(str, Enum):
    BUD = "BUD"
    SNP = "SNP"
    SET = "SET"
    OPR = "OPR"
    CDNX = "CDNX"
    CCC = "CCC"
    HEL = "HEL"
    CCY = "CCY"
    CNQ = "CNQ"
    MCX = "MCX"
    IST = "IST"
    TAL = "TAL"
    NEO = "NEO"
    PSX = "PSX"
    LIT = "LIT"
    RIS = "RIS"
    OSLO = "Oslo"
    TLX = "TLX Exchange"
    INDUSTRY = "Industry"
    XETRA = "XETRA"


class AssetTypes(str, Enum):
    EQUITY = "Equity"
    FUND = "Fund"
    INDEX = "Index"
    ETF = "ETF"
    OPTION = "Option"
    MONEY_MARKET = "MoneyMarket"
    FUTURES = "Futures"
    SHITCOINS = "CRYPTOCURRENCY"
    CURRENCY = "Currency"


class Item(Base):
    name: str
    exchange: Union[UnitedStatesExchanges, ForeignExchanges, OtherExchanges] = Field(
        alias="exchDisp"
    )
    symbol: str
    type: AssetTypes = Field(alias="typeDisp")

    @validator("exchange", pre=True)
    def print_exchange(cls, value):
        if DEBUG_MODE is True:
            if value in [exchange.value for exchange in UnitedStatesExchanges]:
                return value
            elif value in [exchange.value for exchange in ForeignExchanges]:
                return value
            elif value in [exchange.value for exchange in OtherExchanges]:
                return value
            else:
                raise ExchangeNotFoundError(invalid_exchange=value)
        else:
            return value

    @validator("type", pre=True)
    def validate_type(cls, value):
        if DEBUG_MODE is True:
            if value in [asset.value for asset in AssetTypes]:
                return value
            else:
                raise AssetTypeNotFoundError(invalid_asset_type=value)
        else:
            return value


class SymbolAssistResponse(Base):
    items: List[Item]

    def __getitem__(self, index: int):
        if self.items:
            return self.items[index]
        else:
            return None

    def __len__(self):
        return len(self.items)

    def update_items(items: List[Item]):
        self.items = items

    def filter_by_exchange_type(
        self, exchange_type: Union[UnitedStatesExchanges, ForeignExchanges, OtherExchanges]
    ):
        return SymbolAssistResponse(
            items=list(filter(lambda item: item.exchange in exchange_type, self.items))
        )

    def filter_by_asset_type(self, asset_type: AssetTypes):
        return SymbolAssistResponse(
            items=list(filter(lambda item: item.type == asset_type, self.items))
        )


def fuzzy_symbol_seach(
    symbol: str,
    exchange_type: Union[
        UnitedStatesExchanges, ForeignExchanges, OtherExchanges
    ] = UnitedStatesExchanges,
    asset_type: AssetTypes = AssetTypes.EQUITY,
    first=False,
    session=None,
    proxies=None,
    timeout=5,
):
    url = f"https://finance.yahoo.com/_finance_doubledown/api/resource/searchassist;searchTerm={symbol}"

    if session:
        response = session.get(url, proxies=proxies, timeout=timeout)
    else:
        response = requests.get(url, proxies=proxies, timeout=timeout)

    if response.ok:
        try:
            sar = SymbolAssistResponse(**response.json())

        except ValidationError as e:
            print()
            print(e.json(indent=4))
            print()
            raise e

        else:
            sar = sar.filter_by_exchange_type(exchange_type)
            sar = sar.filter_by_asset_type(asset_type)

            if first is True:
                return sar[0]
            else:
                return sar

    return None


#
