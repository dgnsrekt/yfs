import pytest
from yfs.options import parse_option_table, OptionContractType
from pytest_regressions import data_regression  # noqa: F401
from .common_fixtures import option_expiration_data_fixture


# def test_parse_option_table(data_regression, option_expiration_data_fixture):
#     contract_type = OptionContractType.CALL
#     result = parse_option_table(option_expiration_data_fixture)
#     data_regression.check(result.json())
