import pytest
from pytest_regressions import data_regression  # noqa: F401

from yfs.quote import parse_quote_header_info, Quote

from .common_fixtures import summary_page_data_fixture


def test_parse_quote_header_info(data_regression, summary_page_data_fixture):
    result = parse_quote_header_info(summary_page_data_fixture)
    data_regression.check(result.json())
