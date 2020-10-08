"""Module for exchanges organized by region."""

from dataclasses import dataclass
from enum import Enum
from typing import Union

from more_itertools import flatten


class UnitedStatesExchanges(str, Enum):
    """Exchanges based out of the United States."""

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
    """Exchanges Based out of Canda."""

    NATURAL_RESOURCES = "CNQ"
    NEO = "NEO"
    TORONTO = "Toronto"
    VENTURE = "CDNX"


class SouthAmericanExchanges(str, Enum):
    """Exchanges Based out of South America."""

    BUENOS_AIRES = "Buenos Aires"
    MEXICO = "Mexico"
    SAO_PAOLO = "Sao Paolo"
    SANTIAGO = "Santiago Stock Exchange"


class EuropeanExchanges(str, Enum):
    """Exchanges Based out of Europe."""

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
    """Exchanges Based out of Africa."""

    CAIRO = "Cairo Stock Exchange"
    JOHANNESBURG = "Johannesburg Stock Exchange"


class MiddleEasternExchanges(str, Enum):
    """Exchanges Based out of MiddleEast."""

    PAKISTAN = "PSX"
    SAUDI = "Saudi Stock Exchange"
    TEL_AVIV = "Tel Aviv"


class AsianExchanges(str, Enum):
    """Exchanges Based out of Asia."""

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
    """Exchanges Based out of Australia."""

    AUSTRALIAN = "Australian"
    NEW_ZEALAND = "New Zealand"


class UnknownExchanges(str, Enum):
    """Exchanges that haven't been identified yet."""

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
    UNKNOWN = "UNKNOWN"  # placeholder in case all exchanges are identified.


VALID_EXCHANGE_UNION = Union[  # pylint: disable=invalid-name
    UnitedStatesExchanges,
    CanadianExchanges,
    AustralianExchanges,
    AsianExchanges,
    SouthAmericanExchanges,
    EuropeanExchanges,
    MiddleEasternExchanges,
    AfricanExchanges,
    UnknownExchanges,
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
            list(UnknownExchanges),
        ]
    )
)

VALID_EXCHANGE_ENUM_NAMES = [exchange.name for exchange in VALID_EXCHANGE_ENUMS]

VALID_EXCHANGE_ENUM_VALUES = [exchange.value for exchange in VALID_EXCHANGE_ENUMS]


@dataclass
class ExchangeTypes:  # pylint: disable=too-many-instance-attributes, no-member
    """Helper for choosing a valid exchange region.

    This is used for filtering out results from a fuzzy_search request.

    Attributes:
        united_states (Enum): UnitedStatesExchanges
        canada (Enum): CanadianExchanges
        australian (Enum): AustralianExchanges
        asia (Enum): AsianExchanges
        south_america (Enum): SouthAmericanExchanges
        europe (Enum): EuropeanExchanges
        middle_east (Enum): MiddleEasternExchanges
        africa (Enum): AfricanExchanges
        unknown (Enum): UnknownExchanges

    """

    united_states: Enum = UnitedStatesExchanges
    canada: Enum = CanadianExchanges
    australian: Enum = AustralianExchanges
    asia: Enum = AsianExchanges
    south_america: Enum = SouthAmericanExchanges
    europe: Enum = EuropeanExchanges
    middle_east: Enum = MiddleEasternExchanges
    africa: Enum = AfricanExchanges
    unknown: Enum = UnknownExchanges

    @classmethod
    def show(cls) -> None:
        """Print out all valid exchanges."""
        exchange_types = cls().__dataclass_fields__  #
        print("Exchange Types:\n")

        for exchanges in exchange_types:
            print(exchanges)
        print()
