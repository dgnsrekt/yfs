import pytest
from yfs.options import parse_option_table, OptionContractType, get_table_elements
from requests_html import HTML
from pytest_regressions import data_regression  # noqa: F401
from .common_fixtures import option_expiration_data_fixture, option_page_data_fixture


# def test_get_table_elements(option_page_data_fixture):
#     calls_table, puts_table = get_table_elements(option_page_data_fixture)
#     assert 0


# def test_parse_option_table(data_regression, option_expiration_data_fixture):
#     contract_type = OptionContractType.CALL
#     result = parse_option_table(option_expiration_data_fixture)
#     data_regression.check(result.json())
