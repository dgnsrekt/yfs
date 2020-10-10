from itertools import permutations
from pathlib import Path

import pytest

from yfs.paths import TEST_DIRECTORY

from requests_html import HTML


def get_data(path: Path) -> HTML:
    assert path.exists()

    with open(path, mode="r") as file:
        return HTML(html=file.read())


@pytest.fixture(
    params=[
        "aapl",
        "amd",
        "amzn",
        "dia",
        "exfo",
        "fcel",
        "gpro",
        "lite",
        "msft",
        "pavm",
        "tsla",
        "twtr",
    ]
)
def summary_page_data_fixture(request):
    symbol = request.param
    test_response_path = TEST_DIRECTORY / "data" / "summary" / f"{symbol}_summary_page_raw.html"
    return symbol, get_data(test_response_path)


symbols = [
    "aapl",
    "amd",
    "amzn",
    "dia",
    "exfo",
    "fcel",
    "twtr",
]
input = list(permutations(symbols, r=2))
output = [sorted(c) for c in input]


@pytest.fixture(params=list(zip(input, output)))
def multiple_summary_page_data_fixture(request):
    from pprint import pprint

    input, output = request.param
    symbol_one, symbol_two = input

    test_response_path_one = (
        TEST_DIRECTORY / "data" / "summary" / f"{symbol_one}_summary_page_raw.html"
    )
    test_response_path_two = (
        TEST_DIRECTORY / "data" / "summary" / f"{symbol_two}_summary_page_raw.html"
    )
    output = [symbol.upper() for symbol in output]
    return (
        symbol_one,
        symbol_two,
        get_data(test_response_path_one),
        get_data(test_response_path_two),
        output,
    )


#
@pytest.fixture
def option_expiration_data_fixture():
    test_response_path = TEST_DIRECTORY / "data" / "spy_option_expiration_raw.html"
    return get_data(test_response_path)


@pytest.fixture(scope="module", params=["aapl", "exfo", "sar", "tsla"])
def option_page_data_fixture(request):
    symbol = request.param
    test_response_path = TEST_DIRECTORY / "data" / f"{symbol}_option_page_raw.html"
    return get_data(test_response_path)


@pytest.fixture(scope="module", params=["aapl", "fcel"])
def statistics_page_data_fixture(request):
    symbol = request.param
    test_response_path = TEST_DIRECTORY / "data" / f"{symbol}_statistics_page_raw.html"
    return get_data(test_response_path)
