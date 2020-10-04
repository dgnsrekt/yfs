import pytest
from pytest_regressions import data_regression  # noqa: F401

from collections import ChainMap

from yfs.summary import parse_summary_table, SummaryPage
from yfs.quote import parse_quote_header_info

from .common_fixtures import summary_page_data_fixture


def test_parse_summary_table(data_regression, summary_page_data_fixture):

    symbol, data = summary_page_data_fixture

    summary = parse_summary_table(data)
    quote = parse_quote_header_info(data)

    data = ChainMap(quote.dict(), summary)
    data["symbol"] = symbol
    data["quote"] = quote

    result = SummaryPage(**data)

    data_regression.check(result.json())
