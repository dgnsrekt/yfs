"""Contains the classes and functions for using the yahoo finance look up."""

from typing import Iterable, List, Optional, Union

from decouple import config
from pydantic import BaseModel as Base
from pydantic import Field, PydanticValueError, ValidationError, validator

from .asset_types import AssetTypes, VALID_ASSET_TYPES
from .exchanges import UnitedStatesExchanges, VALID_EXCHANGE_ENUM_VALUES, VALID_EXCHANGE_UNION
from .requestor import requestor


RAISE_ERROR_ON_UNKOWN_EXCHANGE_OR_ASSET = config(
    "RAISE_ERROR_ON_UNKOWN_EXCHANGE_OR_ASSET", default=False, cast=bool
)


class ExchangeNotFoundError(PydanticValueError):
    """Raised when an exchange is not found."""

    code = "not_a_valid_exchange"
    msg_template = "Found a missing exchange: {invalid_exchange}. Please raise an issue on github."


class AssetTypeNotFoundError(PydanticValueError):
    """Raised when an assset type is not found."""

    code = "not_a_valid_asset_type"
    msg_template = "Found a missing asset: {invalid_asset_type}. Please raise an issue on github."


class ValidSymbol(Base):
    """A valid symbol response from the yahoo finance quote lookup search bar.

    Attributes:
        symbol (str): A valid ticker symbol abbreviation.
        name (str): Company name.
        exchange (st): A valid market exchange.
            The exchange str will be validated against all of the valid exchange
            enums found in the yfs.exchanges module.
        asset_type (str): A valid asset type.
            The asset type will be validated against the
            yfs.asset_types.AssetTypes enum.

    Example:
    ```python
    {
        "symbol": "AAPL",
        "name": "Apple Inc.",
        "exchange": "NASDAQ",
        "asset_type": "Equity"
    }
    ```
    Notes:
        This class inherits from the pydantic BaseModel which allows for the use
        of .json() and .dict() for serialization to json strings and dictionaries.

        .json(): Serialize to a JSON object.
        .dict(): Serialize to a dictionary.
    """

    symbol: str
    name: str
    exchange: VALID_EXCHANGE_UNION = Field(alias="exchDisp")
    asset_type: AssetTypes = Field(alias="typeDisp")

    class Config:  # noqa: D106 pylint: disable=missing-class-docstring
        allow_population_by_field_name = True

    @validator("exchange", pre=True)
    def check_exchange(cls, value: str) -> str:  # pylint: disable=no-self-argument, no-self-use
        """Check if the exchange is in one of the valid yfs.exchanges enums.

        Raises:
            ExchangeNotFoundError: If the exchange is not one yfs.exchanges enums
                and if the RAISE_ERROR_ON_UNKOWN_EXCHANGE_OR_ASSET environmental variable
                is set to True. (Default) is False.
        """
        if RAISE_ERROR_ON_UNKOWN_EXCHANGE_OR_ASSET is True:

            if value in VALID_EXCHANGE_ENUM_VALUES:
                return value
            raise ExchangeNotFoundError(invalid_exchange=value)
        return value

    @validator("asset_type", pre=True)
    def check_type(cls, value: str) -> str:  # pylint: disable=no-self-argument, no-self-use
        """Check if the asset_type is one of the valid yfs.asset_types enum.

        Raises:
            AssetTypeNotFoundError: If the asset is not found in yfs.asset_types enum
                and if the RAISE_ERROR_ON_UNKOWN_EXCHANGE_OR_ASSET environmental variable
                is set to True. (Default) is False.

        """
        if RAISE_ERROR_ON_UNKOWN_EXCHANGE_OR_ASSET is True:

            if value in VALID_ASSET_TYPES:
                return value
            raise AssetTypeNotFoundError(invalid_asset_type=value)

        return value


class ValidSymbolList(Base):
    """A list of symbol responses from the yahoo finance quote lookup search bar.

    Attributes:
        symbols (ValidSymbol): A list of ValidSymbol's.

    Notes:
        This class inherits from the pydantic BaseModel which allows for the use
        of .json() and .dict() for serialization to json strings and dictionaries.

        .json(): Serialize to a JSON object.
        .dict(): Serialize to a dictionary.

    """

    symbols: List[ValidSymbol] = Field(alias="items")

    class Config:  # noqa: D106 pylint: disable=missing-class-docstring
        allow_population_by_field_name = True

    def __getitem__(self, index: int) -> Optional[ValidSymbol]:
        """Return ValidSymbol at index position."""
        if self.symbols:
            return self.symbols[index]
        return None

    def __len__(self) -> int:
        """Return the amount of symbols."""
        return len(self.symbols)

    def __iter__(self) -> Iterable:
        """Iterate over ValidSymbol objects."""
        return iter(self.symbols)

    # IDEA: Maybe add inplace=True
    def filter_symbols(
        self, exchange_type: VALID_EXCHANGE_UNION, asset_type: AssetTypes
    ) -> "ValidSymbolList":
        """Filter symbols by exchange and asset type.

        Args:
            exchange_type: A valid exchange enum. Example: yfs.exchanges.UnitedStatesExchanges
            asset_type: A valid asset type. Example: yfs.asset_types.AssetTypes.EQUITY

        Returns:
            ValidSymbolList: A new ValidSymbolList with symbols within the exchange and
                asset filters.

        """
        symbols = filter(lambda symbol: symbol.exchange in exchange_type, self.symbols)
        symbols = list(filter(lambda symbol: symbol.asset_type == asset_type, symbols))
        return ValidSymbolList(symbols=symbols)


def fuzzy_search(
    quote_lookup: str,
    exchange_type: VALID_EXCHANGE_UNION = UnitedStatesExchanges,
    asset_type: AssetTypes = AssetTypes.EQUITY,
    first_ticker: bool = True,
    use_filter: bool = False,
    **kwargs,  # noqa: ANN003
) -> Optional[Union[ValidSymbol, ValidSymbolList]]:
    """Lookup and validate symbols or company names.

    Examples:
    ```python
    results = fuzzy_search("apple", first_ticker=False)
    print(results.json(indent=4))
    ```

    ```json
    {
        "symbols": [
            {
                "symbol": "AAPL",
                "name": "Apple Inc.",
                "exchange": "NASDAQ",
                "asset_type": "Equity"
            },
            {
                "symbol": "APLE",
                "name": "Apple Hospitality REIT, Inc.",
                "exchange": "NYSE",
                "asset_type": "Equity"
            },
            ...
        ]
    }
    ```

    ```python
    result = fuzzy_search("aapl", first_ticker=True)
    print(result.json(indent=4))
    ```

    ```json
    {
        "symbol": "AAPL",
        "name": "Apple Inc.",
        "exchange": "NASDAQ",
        "asset_type": "Equity"
    }
    ```

    Args:
        quote_lookup: The company name or symbol to search for.
        exchange_type: One of the yfs.exchanges enums. Default is UnitedStatesExchanges.
        asset_type: One of the yfs.asset_type.AssetTypes. Default is AssetTypes.EQUITY
        first_ticker: If set to true returns the first ValidSymbol in the ValidSymbolList.
            This is normally the best recommended match from the yahoo finance quote lookup.
        **kwargs: Pass (session, proxies, and timeout) to the requestor function.

    Returns:
        ValidSymbol: If first_ticker is set to true and a valid ticker response is found.
        ValidSymbolList: If first_ticker is set to false and a list of valid ticker
            responses are found.
        None: If the yahoo finance quote lookup search returns an empty response or if the
            response did not meet the exchange and asset type filtering requirements.

    Raises:
        ExchangeNotFoundError: If a exchange is found which has not been implemented in one of the
            yfs.exchanges enums. If this error is raised please raise an issue on github with the
            output.
        AssetTypeNotFoundError: If an asset type is not found in the
            yfs.asset_types.AssetTypes enum. If this error is raised please raise and issue on
            github with the output.
    """
    url = (
        "https://finance.yahoo.com/_finance_doubledown/api/"
        f"resource/searchassist;searchTerm={quote_lookup}"
    )

    response = requestor(url, **kwargs)

    if response.ok:

        try:
            search_response = ValidSymbolList(**response.json())

        except ValidationError as error:
            print("\n", error.json(indent=4), "\n")
            raise error

        else:
            if use_filter is True:
                valid_symbols = search_response.filter_symbols(exchange_type, asset_type)
            else:
                valid_symbols = search_response

            if first_ticker is True:
                return valid_symbols[0]  # returns single ValidSymbol

            return valid_symbols  # returns ValidSymbolList

    return None


#
