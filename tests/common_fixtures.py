import pytest

from yfs.paths import TEST_DIRECTORY

from requests_html import HTML


@pytest.fixture
def summary_page_data_fixture():
    test_response_path = TEST_DIRECTORY / "data" / "aapl_summary_page_raw.html"

    assert test_response_path.exists()

    with open(test_response_path, mode="r") as file:
        return HTML(html=file.read())
