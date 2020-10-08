"""A module for asset types."""

from enum import Enum


class AssetTypes(str, Enum):
    """An enum representing all asset types available on yahoo finance.

    AssetTypes is mostly used to filter down choices of assets from the lookup module.
    """

    CURRENCY = "Currency"
    ETF = "ETF"
    EQUITY = "Equity"
    FUND = "Fund"
    FUTURES = "Futures"
    INDEX = "Index"
    MONEY_MARKET = "MoneyMarket"
    OPTION = "Option"
    SHITCOINS = "CRYPTOCURRENCY"


VALID_ASSET_TYPES = [asset.value for asset in AssetTypes]
