from enum import Enum
from typing import Union

from more_itertools import flatten


class UnitedStatesExchanges(str, Enum):
    CBOE = "Chicago Board Options Exchange"
    CBOT = "Chicago Board of Trade"
    CME = "Chicago Mercantile Exchange"
    DOW = "Dow Jones"
    NASDAQ = "NASDAQ"
    NASDAQ_GIDS = "NASDAQ GIDS"
    NSE = "NSE"
    NY_MERCANTILE = "NY Mercantile"
    NYBOT = "New York Board of Trade"
    NYCE = "New York Commodity Exchange"
    NYSE = "NYSE"
    NYSE_MKT = "NYSE MKT"
    NYSE_ARCA = "NYSEArca"
    OTC = "OTC Markets"
    OTC_BB = "OTC BB"


class CanadianExchanges(str, Enum):
    NATURAL_RESOURCES = "CNQ"
    NEO = "NEO"
    TORONTO = "Toronto"
    VENTURE = "CDNX"


class SouthAmericanExchanges(str, Enum):
    BUENOS_AIRES = "Buenos Aires"
    MEXICO = "Mexico"
    SAO_PAOLO = "Sao Paolo"
    SANTIAGO = "Santiago Stock Exchange"


class EuropeanExchanges(str, Enum):
    AMSTERDAM = "Amsterdam"
    ATHENS = "Athens"
    BERLIN = "Berlin"
    BRUSSELS = "Brussels Stock Exchange"
    COPENHAGEN = "Copenhagen"
    DUSSELDORF = "Dusseldorf Stock Exchange"
    EURONEXT = "Euronext"
    FTSE_GLOBAL_INDEX = "FTSEGlobal Index"
    FRANKFURT = "Frankfurt"
    HAMBURG = "Hamburg"
    HANOVER = "Hanover"
    HELSINKI = "HEL"
    IRISH = "Irish"
    ISTANBOL = "IST"
    LISBON = "Lisbon Stock Exchange"
    LONDON = "London"
    LONDON_INTERNATIONAL = "International Orderbook - London"
    MADRID = "Madrid Stock Exchange CATS"
    MILAN = "Milan"
    MUNICH = "Munich"
    NORWAY = "Oslo"
    PARIS = "Paris"
    PRAGUE = "Prague Stock Exchange"
    STOCKHOLM = "Stockholm"
    STUTTGART = "Stuttgart"
    SWISS = "Swiss"
    VIENNA = "Vienna"
    ZURICH = "Zurich Stock Exchange"


class AfricanExchanges(str, Enum):
    CAIRO = "Cairo Stock Exchange"
    JOHANNESBURG = "Johannesburg Stock Exchange"


class MiddleEasternExchanges(str, Enum):
    PAKISTAN = "PSX"
    SAUDI = "Saudi Stock Exchange"
    TEL_AVIV = "Tel Aviv"


class AsianExchanges(str, Enum):
    BOMBAY = "Bombay"
    COLOMBO = "Colombo Stock Exchange"
    HONG_KONG = "Hong Kong"
    JAKARTA = "Jakarta"
    KOREA = "Korea"
    KOSDAQ = "KOSDAQ"
    KUALA_LUMPUR = "Kuala Lumpur Stock Exchange"
    SHENZHEN = "Shenzhen"
    SHANGHAI = "Shanghai"
    SINGAPORE = "Singapore"
    TAIWAN = "Taiwan"
    THAILAND = "SET"
    TOKYO = "Tokyo Stock Exchange"


class AustralianExchanges(str, Enum):
    AUSTRALIAN = "Australian"
    NEW_ZEALAND = "New Zealand"


class UnkownExchanges(str, Enum):
    BUD = "BUD"
    SNP = "SNP"
    OPR = "OPR"
    CCC = "CCC"
    CCY = "CCY"
    MULTI_COMMODITY = "MCX"
    TAL = "TAL"
    LIT = "LIT"
    RIS = "RIS"
    TLX = "TLX Exchange"
    INDUSTRY = "Industry"
    XETRA = "XETRA"
    UNKNOWN = "UNKNOWN"  # placeholder incase all exchanges are identified.


VALID_EXCHANGE_UNION = Union[
    UnitedStatesExchanges,
    CanadianExchanges,
    AustralianExchanges,
    AsianExchanges,
    SouthAmericanExchanges,
    EuropeanExchanges,
    MiddleEasternExchanges,
    AfricanExchanges,
    UnkownExchanges,
]

VALID_EXCHANGE_ENUMS = list(
    flatten(
        [
            list(UnitedStatesExchanges),
            list(CanadianExchanges),
            list(AustralianExchanges),
            list(AsianExchanges),
            list(SouthAmericanExchanges),
            list(EuropeanExchanges),
            list(MiddleEasternExchanges),
            list(AfricanExchanges),
            list(UnkownExchanges),
        ]
    )
)

VALID_EXCHANGE_ENUM_NAMES = [exchange.name for exchange in VALID_EXCHANGE_ENUMS]

VALID_EXCHANGE_ENUM_VALUES = [exchange.value for exchange in VALID_EXCHANGE_ENUMS]
