from typing import List, Optional, Union

from decouple import config
from pydantic import BaseModel as Base
from pydantic import Field, PydanticValueError, ValidationError, validator, validate_arguments

from .asset_types import AssetTypes, VALID_ASSET_TYPES
from .exchanges import UnitedStatesExchanges, VALID_EXCHANGE_ENUM_VALUES, VALID_EXCHANGE_UNION
from .requestor import requestor


RAISE_ERROR_ON_UNKOWN_EXCHANGE_OR_ASSET = config(
    "RAISE_ERROR_ON_UNKOWN_EXCHANGE_OR_ASSET", default=False, cast=bool
)


class ExchangeNotFoundError(PydanticValueError):
    code = "not_a_valid_exchange"
    msg_template = "Found a missing exchange: {invalid_exchange}. Please raise an issue on github."


class AssetTypeNotFoundError(PydanticValueError):
    code = "not_a_valid_asset_type"
    msg_template = "Found a missing asset: {invalid_asset_type}. Please raise an issue on github."


class ValidSymbol(Base):
    """A valid symbol reponse from the yahoo finance quote lookup search bar.

    ValidSymbol inherts from the pydantic base class which allows serialization
    to a dict or json using the .dict() and .json() methods.

    Attributes:
        symbol (str): A valid ticker symbol abbreviation.
        name (str): The company name.
        exchange (st): A valid market exchange.
            The exchange str will be validated against all of the valid exchange
            enums found in the yfs.exchanges module.
        asset_type (str): A valid asset type.
            The asset type will be validated against the
            yfs.asset_types.AssetTypes enum.

    Example:
        ```json
        {
            "symbol": "AAPL",
            "name": "Apple Inc.",
            "exchange": "NASDAQ",
            "asset_type": "Equity"
        }
        ```
    """

    symbol: str
    name: str
    exchange: VALID_EXCHANGE_UNION = Field(alias="exchDisp")
    asset_type: AssetTypes = Field(alias="typeDisp")

    class Config:
        allow_population_by_field_name = True

    @validator("exchange", pre=True)
    def check_exchange(cls, value):
        """Check if the exchange is in one of the valid yfs.exchanges enums

        Raises:
            ExchangeNotFoundError: If the exchange is not in one yfs.exchanges enums
                and if the RAISE_ERROR_ON_UNKOWN_EXCHANGE_OR_ASSET environmental variable
                is set to True. (Default) is False.
        """
        if RAISE_ERROR_ON_UNKOWN_EXCHANGE_OR_ASSET is True:

            if value in VALID_EXCHANGE_ENUM_VALUES:
                return value
            else:
                raise ExchangeNotFoundError(invalid_exchange=value)
        else:
            return value

    @validator("asset_type", pre=True)
    def check_type(cls, value):
        """Checks if the asset_type is one of the valid yfs.asset_types enum.

        Raises:
            AssetTypeNotFoundError: If the asset is not found in yfs.asset_types enum
                and if the RAISE_ERROR_ON_UNKOWN_EXCHANGE_OR_ASSET environmental variable
                is set to True. (Default) is False.

        """
        if RAISE_ERROR_ON_UNKOWN_EXCHANGE_OR_ASSET is True:

            if value in VALID_ASSET_TYPES:
                return value

            else:
                raise AssetTypeNotFoundError(invalid_asset_type=value)
        else:
            return value


class ValidSymbolList(Base):
    """A list of symbol reponses from the yahoo finance quote lookup search bar.

    Attributes:
        symbols (ValidSymbol): A list of ValidSymbol's.

    """

    symbols: List[ValidSymbol] = Field(alias="items")

    class Config:
        allow_population_by_field_name = True

    def __getitem__(self, index: int):
        if self.symbols:
            return self.symbols[index]
        else:
            return None

    def __len__(self):
        return len(self.symbols)

    # IDEA: Maybe add inplace=True
    def filter_symbols(
        self, exchange_type: VALID_EXCHANGE_UNION, asset_type: AssetTypes
    ) -> "ValidSymbolList":
        """Filters symbols by exchange and asset types.

        Args:
            exchange_type: A valid exchange enum. Example: yfs.exchanges.UnitedStatesExchanges
            asset_type: A valid asset type. Example: yfs.asset_types.AssetTypes.EQUITY

        Returns:
            ValidSymbolList: A new ValidSymbolList with symbols within the exchange and
                asset filters.

        """
        return ValidSymbolList(
            symbols=list(
                filter(
                    lambda symbol: symbol.exchange in exchange_type
                    and symbol.asset_type == asset_type,
                    self.symbols,
                )
            )
        )


@validate_arguments
def fuzzy_search(
    quote_lookup: str,
    exchange_type: VALID_EXCHANGE_UNION = UnitedStatesExchanges,
    asset_type: AssetTypes = AssetTypes.EQUITY,
    first_ticker=True,
    **kwargs,
) -> Optional[Union[ValidSymbol, ValidSymbolList]]:
    """Uses the yahoo finance quote lookup to validate symbols or company names.

    Examples:
        results = fuzzy_search("apple", first_ticker=False)
        print(results.json(indent=4))
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

        result = fuzzy_search("aapl", first_ticker=True)
        print(result.json(indent=4))
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
        exchange_type: One of the yfs.exchanges enums. Default is UnitedStatesExchanges
        asset_type: One of the yfs.asset_type.AssetTypes. Default is AssetTypes.EQUITY
        first_ticker: If set to true returns the first ValidSymbol in the ValidSymbolList.
            This is normally the best recommended match from the yahoo finance quote lookup.
        session: Gives the ability to pass a Session object for continuous use.
        proxies: Any proxies to pass to the requestor function.
        timeout: The request timeout.

    Returns:
        ValidSymbol: If first_ticker is set to true and a valid ticker response is found.
        ValidSymbolList: if first_ticker is set to false and a list of valid ticker
            responses are found.
        None: If the yahoo finance quote lookup search returns an empty response or if the
            response did not meet the exchange and asset type filtering.

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

        except ValidationError as e:
            print("\n", e.json(indent=4), "\n")
            raise e

        else:
            valid_symbols = search_response.filter_symbols(exchange_type, asset_type)

            if first_ticker is True:
                return valid_symbols[0]  # returns single ValidSymbol
            else:
                return valid_symbols  # returns ValidSymbolList

    return None


#
