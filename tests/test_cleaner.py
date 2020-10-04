import pytest

from yfs.cleaner import CommonCleaners, field_cleaner


field_test_params = {
    "Previous Close": "previous_close",
    "Open": "open",
    "Bid": "bid",
    "Ask": "ask",
    "Day's Range": "days_range",
    "52 Week Range": "fifty_two_week_range",
    "Volume": "volume",
    "Avg. Volume": "avg_volume",
    "Market Cap": "market_cap",
    "Beta (5Y Monthly)": "beta_five_year_monthly",
    "PE Ratio (TTM)": "pe_ratio_ttm",
    "EPS (TTM)": "eps_ttm",
    "Earnings Date": "earnings_date",
    "Forward Dividend & Yield": "forward_dividend_yield",
    "Ex-Dividend Date": "exdividend_date",
    "1y Target Est": "one_year_target_est",
}


@pytest.mark.parametrize("fields", field_test_params.items())
def test_field_cleaner(fields):
    field, target = fields
    result = field_cleaner(field)
    assert result == target


remove_comma_params = {
    "112.28": "112.28",
    "115.01": "115.01",
    "112.25 x 1100": "112.25 x 1100",
    "112.28 x 2200": "112.28 x 2200",
    "112.78 - 115.32": "112.78 - 115.32",
    "53.15 - 137.98": "53.15 - 137.98",
    "137,672,403": "137672403",
    "172,504,452": "172504452",
    "1.966T": "1.966T",
    "1.28": "1.28",
    "34.07": "34.07",
    "3.30": "3.30",
    "Oct 28, 2020 - Nov 02, 2020": "Oct 28 2020 - Nov 02 2020",
    "0.82 (0.76%)": "0.82 (0.76%)",
    "Aug 07, 2020": "Aug 07 2020",
    "119.25": "119.25",
}


@pytest.mark.parametrize("values", remove_comma_params.items())
def test_remove_comma(values):
    value, target = values
    result = CommonCleaners.remove_comma(value)
    assert result == target


remove_brakets_params = {
    "112.28": "112.28",
    "115.01": "115.01",
    "112.25 x 1100": "112.25 x 1100",
    "112.28 x 2200": "112.28 x 2200",
    "112.78 - 115.32": "112.78 - 115.32",
    "53.15 - 137.98": "53.15 - 137.98",
    "137,672,403": "137,672,403",
    "172,504,452": "172,504,452",
    "1.966T": "1.966T",
    "1.28": "1.28",
    "34.07": "34.07",
    "3.30": "3.30",
    "Oct 28, 2020 - Nov 02, 2020": "Oct 28, 2020 - Nov 02, 2020",
    "0.82 0.76%": "0.82 0.76%",
    "Aug 07, 2020": "Aug 07, 2020",
    "119.25": "119.25",
}


@pytest.mark.parametrize("values", remove_brakets_params.items())
def test_remove_brakets(values):
    value, target = values
    result = CommonCleaners.remove_brakets(value)
    assert result == target


remove_percent_sign_params = {
    "112.28": "112.28",
    "115.01": "115.01",
    "112.25 x 1100": "112.25 x 1100",
    "112.28 x 2200": "112.28 x 2200",
    "112.78 - 115.32": "112.78 - 115.32",
    "53.15 - 137.98": "53.15 - 137.98",
    "137,672,403": "137,672,403",
    "172,504,452": "172,504,452",
    "1.966T": "1.966T",
    "1.28": "1.28",
    "34.07": "34.07",
    "3.30": "3.30",
    "Oct 28, 2020 - Nov 02, 2020": "Oct 28, 2020 - Nov 02, 2020",
    "0.82 (0.76%)": "0.82 (0.76)",
    "Aug 07, 2020": "Aug 07, 2020",
    "119.25": "119.25",
}


@pytest.mark.parametrize("values", remove_percent_sign_params.items())
def test_remove_percent_sign(values):
    value, target = values
    result = CommonCleaners.remove_percent_sign(value)
    assert result == target


value_is_missing_params = {
    "112.28": False,
    "115.01": False,
    "112.25 x 1100": False,
    "112.28 x 2200": False,
    "112.78 - 115.32": False,
    "53.15 - 137.98": False,
    "137,672,403": False,
    "172,504,452": False,
    "1.966T": False,
    "1.28": False,
    "34.07": False,
    "3.30": False,
    "Oct 28, 2020 - Nov 02, 2020": False,
    "0.82 (0.76%)": False,
    "Aug 07, 2020": False,
    "119.25": False,
    "N/A": True,
    "N/A (N/A)": True,
    "0.75 (N/A)": True,
    "N/A (-7.34)": True,
    "N/A x N/A": True,
    "112.23 x N/A": True,
    "N/A x 2200": True,
    "N/A - N/A": True,
    "112.23 - N/A": True,
    "N/A - 2200": True,
    "undefined": True,
    "undefined - undefined": True,
    "2.30 - undefined": True,
    "undefined - 47.34": True,
    "+-34.23%": True,
    "-+7.43%": True,
    "": True,
    " ": True,
    "  2.4%": False,
    2.0: False,
    750: False,
}


@pytest.mark.parametrize("values", value_is_missing_params.items())
def test_value_is_missing(values):
    value, target = values
    result = CommonCleaners.value_is_missing(value)
    assert result == target


has_number_suffix_params = {
    "112.28": False,
    "115.01": False,
    "112.25 x 1100": False,
    "112.28 x 2200": False,
    "112.78 - 115.32": False,
    "53.15 - 137.98": False,
    "137,672,403": False,
    "172,504,452": False,
    "1.966T": True,
    "1.28B": True,
    "34.07M": True,
    "3.30K": True,
    "0.82 (0.76%)": False,
    "119.25": False,
}


@pytest.mark.parametrize("values", has_number_suffix_params.items())
def test_has_number_suffix(values):
    value, target = values
    result = CommonCleaners.has_large_number_suffix(value)
    assert result == target


clean_number_with_suffix_params = {
    "115.01": None,
    "1.966T": 1_966_000_000_000,
    "1.28B": 1_280_000_000,
    "34.07M": 34_070_000,
    "3.30K": 3_300,
    "119.25": None,
}


@pytest.mark.parametrize("values", clean_number_with_suffix_params.items())
def test_clean_number_with_suffix(values):
    value, target = values
    result = CommonCleaners.clean_large_number(value)
    assert result == target


common_value_cleaner_params = {
    "115.01": "115.01",
    "137,672,403": "137672403",
    "172,504,452": "172504452",
    "1.966T": 1_966_000_000_000,
    "1.28B": 1_280_000_000,
    "34.07M": 34_070_000,
    "3.30K": 3_300,
    "119.25": "119.25",
    "N/A": "N/A",
}


@pytest.mark.parametrize("values", common_value_cleaner_params.items())
def test_common_value_cleaner(values):
    value, target = values
    result = CommonCleaners.common_value_cleaner(value)
    assert result == target


clean_common_values_params = {
    "115.01": "115.01",
    "137,672,403": "137672403",
    "172,504,452": "172504452",
    "1.966T": 1_966_000_000_000,
    "1.28B": 1_280_000_000,
    "34.07M": 34_070_000,
    "3.30K": 3_300,
    "119.25": "119.25",
    "N/A": None,
    "undefined": None,
    "undefined - undefined": None,
}


@pytest.mark.parametrize("values", clean_common_values_params.items())
def test_common_value_cleaner(values):
    value, target = values
    result = CommonCleaners.clean_common_values(value)
    assert result == target


clean_basic_percentage_params = {
    "112.28": "112.28",
    "115.01": "115.01",
    "112.25 x 1100": "112.25 x 1100",
    "112.28 x 2200": "112.28 x 2200",
    "112.78 - 115.32": "112.78 - 115.32",
    "53.15 - 137.98": "53.15 - 137.98",
    "137,672,403": "137672403",
    "172,504,452": "172504452",
    "1.966T": "1.966T",
    "1.28": "1.28",
    "34.07": "34.07",
    "3.30": "3.30",
    "0.82 (0.76%)": "0.82 (0.76)",
    "119.25": "119.25",
    "N/A": None,
    "undefined": None,
    "undefined - undefined": None,
}


@pytest.mark.parametrize("values", clean_basic_percentage_params.items())
def test_common_value_cleaner(values):
    value, target = values
    result = CommonCleaners.clean_basic_percentage(value)
    assert result == target


clean_dates_params = {
    "Oct 28, 2020 - Nov 02, 2020": "2020-10-28T00:00:00+00:00",
    "Aug 07, 2020": "2020-08-07T00:00:00+00:00",
}


@pytest.mark.parametrize("values", clean_dates_params.items())
def test_clean_date(values):
    value, target = values
    result = CommonCleaners.clean_date(value)
    assert str(result) == target


def test_clean_symbol():
    before = "aapl"
    target = "AAPL"
    result = CommonCleaners.clean_symbol(before)
    assert target == result


clean_first_value_split_by_dash_params = {
    "112.78 - 115.32": "112.78",
    "53.15 - 137.98": "53.15",
}


@pytest.mark.parametrize("values", clean_first_value_split_by_dash_params.items())
def test_clean_first_value_split_by_dash(values):
    value, target = values
    result = CommonCleaners.clean_first_value_split_by_dash(value)
    assert str(result) == target


clean_second_value_split_by_dash_params = {
    "112.78 - 115.32": "115.32",
    "53.15 - 137.98": "137.98",
}


@pytest.mark.parametrize("values", clean_second_value_split_by_dash_params.items())
def test_clean_second_value_split_by_dash(values):
    value, target = values
    result = CommonCleaners.clean_second_value_split_by_dash(value)
    assert str(result) == target


clean_first_value_split_by_x_params = {
    "112.25 x 1100": "112.25",
    "112.28 x 2200": "112.28",
}


@pytest.mark.parametrize("values", clean_first_value_split_by_x_params.items())
def test_clean_first_value_split_by_x(values):
    value, target = values
    result = CommonCleaners.clean_first_value_split_by_x(value)
    assert str(result) == target


clean_second_value_split_by_x_params = {
    "112.25 x 1100": "1100",
    "112.28 x 2200": "2200",
}


@pytest.mark.parametrize("values", clean_second_value_split_by_x_params.items())
def test_clean_second_value_split_by_x(values):
    value, target = values
    result = CommonCleaners.clean_second_value_split_by_x(value)
    assert str(result) == target
