import json
import pytest
from pytest_regressions import data_regression  # noqa: F401

from pydantic import ValidationError

from yfs.lookup import ValidSymbol, ValidSymbolList
from yfs.paths import TEST_DIRECTORY

from yfs.exchanges import (
    EuropeanExchanges,
    SouthAmericanExchanges,
    UnitedStatesExchanges,
    UnknownExchanges,
)
from yfs.asset_types import AssetTypes


@pytest.fixture
def quote_lookup_raw_response():
    test_response_path = TEST_DIRECTORY / "data" / "aapl_quote_lookup_raw_response.json"

    assert test_response_path.exists()

    with open(test_response_path, mode="r") as file:
        return json.load(file)


def test_valid_symbol_object(data_regression):
    results = ValidSymbol(symbol="aapl", name="Apple Inc.", exchange="NASDAQ", asset_type="Equity")
    data_regression.check(results.json())


def test_valid_symbol_list_object(data_regression, quote_lookup_raw_response):
    results = ValidSymbolList(**quote_lookup_raw_response)
    data_regression.check(results.json())


valid_symbol_list_filter_parameters = [
    (UnitedStatesExchanges, AssetTypes.EQUITY),
    (UnitedStatesExchanges, AssetTypes.INDEX),
    (UnknownExchanges, AssetTypes.EQUITY),
    (SouthAmericanExchanges, AssetTypes.EQUITY),
    (EuropeanExchanges, AssetTypes.EQUITY),
]


@pytest.mark.parametrize("exchange_type,asset_type", valid_symbol_list_filter_parameters)
def test_valid_symbol_list_filer(
    data_regression, quote_lookup_raw_response, exchange_type, asset_type
):
    before = ValidSymbolList(**quote_lookup_raw_response)

    after_filtering = before.filter_symbols(exchange_type=exchange_type, asset_type=asset_type)

    data_regression.check(after_filtering.json())


def test_raises_validation_error_with_invalid_exchange():
    with pytest.raises(ValidationError):
        ValidSymbol(
            symbol="aapl", name="Apple Inc.", exchange="FAKE_EXCHANGE", asset_type="Equity"
        )


def test_raises_validation_error_with_invalid_asset_type():
    with pytest.raises(ValidationError):
        ValidSymbol(symbol="aapl", name="Apple Inc.", exchange="NASDAQ", asset_type="FAKE_ASSET")
