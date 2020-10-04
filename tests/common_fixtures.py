from pathlib import Path

import pytest

from yfs.paths import TEST_DIRECTORY

from requests_html import HTML


def get_data(path: Path) -> HTML:
    assert path.exists()

    with open(path, mode="r") as file:
        return HTML(html=file.read())


@pytest.fixture(params=["aapl"])
def summary_page_data_fixture(request):
    symbol = request.param
    test_response_path = TEST_DIRECTORY / "data" / f"{symbol}_summary_page_raw.html"
    return symbol, get_data(test_response_path)


@pytest.fixture
def option_expiration_data_fixture():
    test_response_path = TEST_DIRECTORY / "data" / "spy_option_expiration_raw.html"
    return get_data(test_response_path)


@pytest.fixture(scope="module", params=["aapl", "fcel"])
def statistics_page_data_fixture(request):
    symbol = request.param
    test_response_path = TEST_DIRECTORY / "data" / f"{symbol}_statistics_page_raw.html"
    return get_data(test_response_path)
