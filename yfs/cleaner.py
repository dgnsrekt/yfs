"""A module for cleaning tables, fields and values."""

from functools import partial
from typing import Dict, Optional, Union

import pendulum
from pendulum import DateTime
from pydantic import validator
from requests_html import HTML


numbers_with_suffix = {
    "T": 1_000_000_000_000,
    "B": 1_000_000_000,
    "M": 1_000_000,
    "K": 1_000,
}


def field_cleaner(field: str) -> str:
    """Convert field string from an html response into a snake case variable.

    Args:
        field (str): A dirty field string.

    Example:
        |Input             |  Output                |
        |------------------|------------------------|
        |Previous Close    | previous_close         |
        |Avg. Volume       | avg_volume             |
        |Beta (5Y Monthly) | beta_five_year_monthly |
        |PE Ratio (TTM)    | pe_ratio_ttm           |

    Returns:
        str: lowercased and converted to snake case.
    """
    return (
        field.lower()
        .replace("(", "")
        .replace(")", "")
        .replace("'", "")
        .replace(".", "")
        .replace("& ", "")
        .replace("-", "")
        .replace("52", "fifty_two")
        .replace("5y", "five_year")
        .replace("1y", "one_year")
        .replace(" ", "_")
        .replace("5_yr", "five_year")
        .replace("5_year", "five_year")
        .replace("200day", "two_hundred_day")
        .replace("50day", "fifty_day")
        .replace("/", "_")
        .replace("&", "")
        .replace("%", "percent")
        .replace("10_day", "ten_day")
        .replace("3_month", "three_month")
        .strip()
    )


def table_cleaner(html_table: HTML) -> Optional[Dict]:
    """Clean table with two fields.

    Args:
        html_table (HTML): HTML object parsed from a table section.

    Returns:
        dict: cleaned fields (keys) and string (values).
        None: if html_table does not contain table elements.
    """
    rows = [row.text.split("\n") for row in html_table.find("tr")]
    rows = list(filter(lambda row: len(row) == 2, rows))

    data = {}

    for field, value in rows:
        field = field_cleaner(field)
        data[field] = value

    if data:
        return data

    return None


cleaner = partial(validator, pre=True, allow_reuse=True)
"""* Partial overloading the pytdanitc.validator function with common args."""


class CommonCleaners:
    """Contains the most commonly used methods for cleaning values."""

    @staticmethod
    def remove_comma(value: str) -> str:
        """Remove commas from strings and strip whitespace.

        Args:
            value (str): A number with more than 3 digits.

        Example:
            |Input   | Output|
            |--------|-------|
            |'5,000' | '5000'|

        Returns:
            str: Commas removed and whitespace stripped.
        """
        return value.replace(",", "").strip()

    @staticmethod
    def remove_brakets(value: str) -> str:
        """Remove () brakets from strings and strip whitespace.

        Args:
            value (str): Containing () brakets. Normally surrounding a percent change.

        Example:
            |Input           |Output       |
            |----------------|-------------|
            |+19.60 (+1.36%) |+19.60 +1.36 |

        Returns:
            str: () brakets removed and whitespace stripped.
        """
        return value.replace("(", "").replace(")", "").strip()

    @staticmethod
    def remove_percent_sign(value: str) -> str:
        """Remove percent sign % from string and strip whitespace.

        Args:
            value (str): Containing percent sign.

        Example:
            |Input     |Output |
            |----------|-------|
            |+1.36%    |+1.36  |

        Returns:
            str: Percent sign % removed and whitespace stripped.
        """
        return value.replace("%", "").strip()

    @classmethod
    def remove_brakets_and_percent_sign(cls, value: str) -> str:
        """Remove () brakets and % percent signs from string.

        Args:
            value (str): Contains () backets and % percent sign.

        Example:
            |Input              |Output      |
            |-------------------|------------|
            |+19.60 (+1.36%)    |+19.60 +1.36|

        Returns:
            str: () brakets % percent sign removed.
        """
        value = cls.remove_brakets(value)
        return cls.remove_percent_sign(value)

    @staticmethod
    def value_is_missing(value: str) -> bool:
        """Check if value has missing data.

        It checks to see if "N/A" and other missing data strings are present in the value.

        Args:
            value (str): A value parsed from yahoo finance.

        Example:
            |Input                    |Output      |
            |-------------------------|------------|
            |"Ex-Dividend Date    N/A"|True        |

        Returns:
            bool: True if a missing data string is found in value else False.

        """
        if not isinstance(value, str):
            return False

        missing_values = [
            "N/A",
            "undefined",
            "+-",
            "-+",
        ]

        for missing in missing_values:
            if missing in value:
                return True

        other_missing = ["", " ", "-"]

        for missing in other_missing:
            if value == missing:
                return True

        return False

    @staticmethod
    def has_large_number_suffix(value: str) -> bool:
        """Check if string representation of a number has T,B,M,K suffix.

        Args:
            value (str): A value to check if contains a T,B,M,K suffix.

        Example:

            |Input  |Output      |
            |-------|------------|
            |225.0M |True        |

        Returns:
            bool: True if string value contains T,B,M,K suffix else false.
        """
        for suffix, _ in numbers_with_suffix.items():
            if suffix in value.upper():
                return True

        return False

    @staticmethod
    def clean_large_number(value: str) -> Optional[int]:
        """Convert a string representation of a number with a T,B,M,K suffix to an int.

        Args:
            value (str): A value which contains T,B,M,K suffix.

        Example:
            |Input |Output       |
            |------|-------------|
            |2.5B  |2_500_000_000|

        Returns:
            int: suffix removed and used as multiplier to convert to an int.
            None: This can return None, but should not because the
                has_large_number_suffix method should be used to check if
                this method should even be run.
        """
        value = value.upper()

        for suffix, multiplier in numbers_with_suffix.items():
            if suffix in value:
                return round(float(value.replace(suffix, "")) * multiplier)

        return None

    @classmethod
    def common_value_cleaner(cls, value: str) -> Union[int, str]:
        """Most common method for cleaning most values from yahoo finance.

        Removes commas and converts number if it has a suffix.

        Args:
            value (str): value to be cleaned.

        Example:
            |Input   |Output       |Type|
            |--------|-------------|----|
            |"5,000" | "5000"      |str |
            |"2.5M"  | 2_500_000   |int |

        Returns:
            str: If value is cleaned and doesn't have a suffix.
            int: If value is cleaned and has a suffix.

        """
        value = cls.remove_comma(value)

        if cls.has_large_number_suffix(value):
            value = cls.clean_large_number(value)

        return value

    @classmethod
    def clean_common_values(cls, value: str) -> Optional[Union[int, str]]:
        """Most common vanilla method for cleaning most values with a check for missing values.

        Args:
            value (str): value to be cleaned.

        Example:
            |Input      |Output    |Type|
            |-----------|----------|----|
            |"5,000"    |"5000"    |str |
            |"2.5M"     |2_500_000 |int |
            |"N/A"      |None      |None|

        Returns:
            str:  If value is cleaned and doesn't have a suffix.
            int:  If value is cleaned and has a suffix.
            None: If value is missing.
        """
        if cls.value_is_missing(value):
            return None
        return cls.common_value_cleaner(value)

    @classmethod
    def clean_basic_percentage(cls, value: str) -> Optional[str]:
        """Clean a single percentage value.

        Args:
            value (str): value to be cleaned.

        Example:
            |Input   |Output |Type|
            |--------|-------|----|
            |"-3.4%" |"-3.4" |str |
            |"N/A"   |None   |None|

        Returns:
            str: cleaned value if value is not missing.
            None: if value is missing.
        """
        if cls.value_is_missing(value):
            return None
        value = cls.remove_percent_sign(value)
        return cls.remove_comma(value)

    @classmethod
    def clean_date(cls, value: str) -> DateTime:
        """Clean and convert a string date.

        Uses pendulum parse method to extract datetime information. Sometimes yahoo
        finance give multiple dates in one value field. This normally happens in the
        Earnings Date section on the Summary page. The Earnings Date may have a single
        date or an estimated Earnings Date range. It would be very easy to have this method
        output a pendulum.period.Period object that can represent the date range. The
        decision was made to just return the start of the earnings period for consistency.

        Args:
            value (str): Date string to be converted to datetime object.

        Example:
            |Input                                         |Output                            |
            |----------------------------------------------|----------------------------------|
            |"Earnings Date    Oct 26, 2020 - Oct 30, 2020"|DateTime 2020-10-26T00:00:00+00:00|

        Returns:
            str: cleaned if value is not missing.
            None: if value is missing.
        """
        if cls.value_is_missing(value):
            return None

        dates = value.split("-")

        if len(dates) > 1:
            start, _ = dates
            start = pendulum.parse(start, strict=False)
            return start

        return pendulum.parse(value, strict=False)

    @classmethod
    def clean_symbol(cls, value: str) -> str:
        """Make symbol uppercase.

        Args:
            value (str): Stock symbol.

        Example:
            |Input |Output |
            |------|-------|
            |aapl  |AAPL   |

        Returns:
            str: Uppercased.
        """
        return value.upper()

    @classmethod
    def clean_first_value_split_by_dash(cls, value: str) -> str:
        """Split value separated by '-' and return the first value.

        Args:
            value (str): A string with multiple values separated by a '-'.

        Example:
            |Input            |Output  |
            |-----------------|--------|
            |"2.3400 - 2.4900"|"2.3400"|

        Returns:
            strs: First value parse from string.
            None: if value is missing.
        """
        if cls.value_is_missing(value):
            return None

        value, _ = value.split("-")
        return cls.common_value_cleaner(value)

    @classmethod
    def clean_second_value_split_by_dash(cls, value: str) -> str:
        """Split value separated by '-' and return the second value.

        Args:
            value (str): A string with multiple values separated by a '-'.

        Example:
            |Input            |Output  |
            |-----------------|--------|
            |"2.3400 - 2.4900"|"2.4900"|

        Returns:
            strs: Second value parse from string.
            None: if value is missing.
        """
        if cls.value_is_missing(value):
            return None

        _, value = value.split("-")
        value = cls.common_value_cleaner(value)
        return value

    @classmethod
    def clean_first_value_split_by_space(cls, value: str) -> str:
        """Clean first string containing a change and percent.

        This will strip brakets and percent sign leaving only a whitespace
        between the change and percent change. Next it will split the values then
        return the first value. Normally the Forward Dividend & Yield from the
        summary page.

        Args:
            value (str): Normally a string containing change and percent change.

        Example:
            |Input            |Output  |
            |-----------------|--------|
            |"0.82 (0.73%)"   |"0.82"  |

        Returns:
            str: The first string.
            None: if value is missing.
        """
        if cls.value_is_missing(value):
            return None

        value, _ = cls.remove_brakets_and_percent_sign(value).split(" ")
        return value

    @classmethod
    def clean_second_value_split_by_space(cls, value: str) -> str:
        """Clean second string containing a change and percent.

        This will strip brakets and percent sign leaving only a whitespace
        between the change and percent change. Next it will split the values then
        return the second value. Normally the Forward Dividend & Yield from the
        summary page.

        Args:
            value (str): Normally a string containing change and percent change.

        Example:
            |Input            |Output  |
            |-----------------|--------|
            |"0.82 (0.73%)"   |"0.73"  |

        Returns:
            str: The Second value.
            None: if value is missing.
        """
        if cls.value_is_missing(value):
            return None

        _, percentage = cls.remove_brakets_and_percent_sign(value).split(" ")
        return percentage

    @classmethod
    def clean_first_value_split_by_x(cls, value: str) -> str:
        """Split value separated by 'x' and return the first value.

        Args:
            value (str): A string with multiple values separated by a 'x'.

        Example:
            |Input            |Output  |
            |-----------------|--------|
            |"2.4000 x 21500" |"2.4000"|

        Returns:
            strs: First value parse from string.
            None: if value is missing.
        """
        if cls.value_is_missing(value):
            return None

        price, _ = value.split("x")
        return cls.common_value_cleaner(price)

    @classmethod
    def clean_second_value_split_by_x(cls, value: str) -> str:
        """Split value separated by 'x' and return the second value.

        Args:
            value (str): A string with multiple values separated by a 'x'.

        Example:
            |Input            |Output  |
            |-----------------|--------|
            |"2.4000 x 21500" |"21500" |

        Returns:
            strs: Second value parse from string.
            None: if value is missing.
        """
        if cls.value_is_missing(value):
            return None

        _, volume = value.split("x")
        return cls.common_value_cleaner(volume)
