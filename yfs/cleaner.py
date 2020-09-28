from functools import partial

import pendulum
from pydantic import BaseModel as Base
from pydantic import validator


class large_numer_suffix(Base):
    T: int = 1_000_000_000_000  # big boys
    B: int = 1_000_000_000  # average useless tech
    M: int = 1_000_000  # lol who cares
    K: int = 1_000


def field_cleaner(field):
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


def table_cleaner(html_table):
    rows = [row.text.split("\n") for row in html_table.find("tr")]
    rows = list(filter(lambda row: len(row) == 2, rows))

    data = {}

    for field, value in rows:
        field = field_cleaner(field)
        data[field] = value

    if data:
        return data
    else:
        return None


cleaner = partial(validator, pre=True, allow_reuse=True)


class CommonCleaners:
    @staticmethod
    def remove_comma(value: str):
        return value.replace(",", "").strip()

    @staticmethod
    def remove_brakets(value: str):
        return value.replace("(", "").replace(")", "").strip()

    @staticmethod
    def remove_percent_sign(value: str):
        return value.replace("%", "").strip()

    @classmethod
    def remove_brakets_and_precent_sign(cls, value: str):
        value = cls.remove_brakets(value)
        return cls.remove_percent_sign(value)

    @staticmethod
    def value_is_missing(value):
        if not isinstance(value, str):
            return False

        if "N/A" in value:
            # Should take care of the following invalid data:
            #     "N/A"
            #     "N/A (N/A)"
            #     "N/A x N/A"
            #     "N/A - N/A"
            return True

        elif "undefined" in value:  # "undefined - undefined"
            return True
        elif "+-" in value:  # ¯\_(ツ)_/¯ it happens.
            return True
        elif "-+" in value:
            return True
        elif value == "":  # just incase
            return True
        elif value == " ":
            return True
        elif value == "-":  # These show up on the option page
            return True
        else:
            return False

    @staticmethod
    def has_large_number_suffix(value: str):
        for suffix, _ in large_numer_suffix():
            if suffix in value.upper():
                return True
        else:
            return False

    @staticmethod
    def clean_large_number(value: str):
        value = value.upper()
        for suffix, multiplier in large_numer_suffix():
            if suffix in value:
                return round(float(value.replace(suffix, "")) * multiplier)

    @classmethod
    def common_value_cleaner(cls, value: str):
        value = cls.remove_comma(value)

        if cls.has_large_number_suffix(value):
            value = cls.clean_large_number(value)

        return value

    @classmethod
    def clean_common_values(cls, value):
        if cls.value_is_missing(value):
            return None
        return cls.common_value_cleaner(value)

    @classmethod
    def clean_basic_percentage(cls, value):
        if cls.value_is_missing(value):
            return None
        value = cls.remove_percent_sign(value)
        return cls.remove_comma(value)

    @classmethod
    def clean_date(cls, value: str):
        if cls.value_is_missing(value):
            return None

        dates = value.split("-")

        if len(dates) > 1:
            start, end = dates

            start = pendulum.parse(start, strict=False)
            # end = pendulum.parse(end, strict=False)

            return start
        else:
            return pendulum.parse(value, strict=False)

    @classmethod
    def clean_symbol(cls, value: str):
        return value.upper()

    @classmethod
    def clean_first_value_split_by_dash(cls, value):
        if cls.value_is_missing(value):
            return None

        _, value = value.split("-")
        value = cls.common_value_cleaner(value)
        return value

    @classmethod
    def clean_second_value_split_by_dash(cls, value):
        if cls.value_is_missing(value):
            return None

        _, value = value.split("-")
        value = cls.common_value_cleaner(value)
        return value

    @classmethod
    def clean_first_value_split_by_space(cls, value):
        if cls.value_is_missing(value):
            return None

        value, _ = cls.remove_brakets_and_precent_sign(value).split(" ")
        return value

    @classmethod
    def clean_second_value_split_by_space(cls, value):
        if cls.value_is_missing(value):
            return None

        _, percentage = cls.remove_brakets_and_precent_sign(value).split(" ")
        return percentage

    @classmethod
    def clean_first_value_split_by_x(cls, value):
        if cls.value_is_missing(value):
            return None

        price, _ = value.split("x")
        return cls.common_value_cleaner(price)

    @classmethod
    def clean_second_value_split_by_x(cls, value):
        if cls.value_is_missing(value):
            return None

        _, volume = value.split("x")
        return cls.common_value_cleaner(volume)
