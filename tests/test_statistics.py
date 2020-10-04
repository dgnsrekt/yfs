import pytest
from yfs.statistics import (
    parse_valuation_table,
    parse_financial_highlights_table,
    parse_trading_information_table,
)
from pytest_regressions import data_regression  # noqa: F401
from .common_fixtures import statistics_page_data_fixture


def test_parse_valuation_table(data_regression, statistics_page_data_fixture):
    result = parse_valuation_table(statistics_page_data_fixture)
    data_regression.check(result.json())


def test_financial_highlights_table(data_regression, statistics_page_data_fixture):
    result = parse_financial_highlights_table(statistics_page_data_fixture)
    data_regression.check(result.json())


def test_parse_trading_information_table(data_regression, statistics_page_data_fixture):
    result = parse_trading_information_table(statistics_page_data_fixture)
    data_regression.check(result.json())
