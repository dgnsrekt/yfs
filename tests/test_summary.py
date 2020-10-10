import pytest
from pytest_regressions import data_regression  # noqa: F401

from collections import ChainMap

from yfs.summary import parse_summary_table, SummaryPage, SummaryPageGroup
from yfs.quote import parse_quote_header_info

from .common_fixtures import summary_page_data_fixture, multiple_summary_page_data_fixture


def create_summary_page_object(symbol, data):
    summary = parse_summary_table(data)
    quote = parse_quote_header_info(data)

    data = ChainMap(quote.dict(), summary)
    data["symbol"] = symbol
    data["quote"] = quote

    return SummaryPage(**data)


def test_parse_summary_table(data_regression, summary_page_data_fixture):

    symbol, data = summary_page_data_fixture

    result = create_summary_page_object(symbol, data)

    assert result.high > result.low

    data_regression.check(result.json())


def test_sorting_summary_pages(multiple_summary_page_data_fixture):
    symbol_one, symbol_two, data_one, data_two, target = multiple_summary_page_data_fixture
    page_one = create_summary_page_object(symbol_one, data_one)
    page_two = create_summary_page_object(symbol_two, data_two)

    summary_page_group = SummaryPageGroup()

    summary_page_group.append(page_one)
    summary_page_group.append(page_two)
    summary_page_group.sort()
    assert summary_page_group.symbols == target
