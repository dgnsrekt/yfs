from typing import Optional

from pydantic import BaseModel as Base
from pydantic import validator as clean
from requests_html import HTML

from .cleaner import ValueCleanerBase


class Quote(ValueCleanerBase):
    name: str
    close: Optional[float]
    change: Optional[float]
    percent_change: Optional[float]

    @clean("name", pre=True)
    def clean_name(cls, value):
        value = value.split("(")
        return value[0].strip()

    @clean("close", pre=True)
    def clean_close(cls, value):
        if cls.value_is_missing(value):
            return None
        return cls.common_value_cleaner(value)

    @clean("change", pre=True)
    def clean_change(cls, value):
        if cls.value_is_missing(value):
            return None
        change, _ = cls.remove_brakets_and_precent_sign(value).split(" ")
        return change

    @clean("percent_change", pre=True)
    def clean_percent_change(cls, value):
        if cls.value_is_missing(value):
            return None
        _, percent_change = cls.remove_brakets_and_precent_sign(value).split(" ")
        return percent_change


def parse_quote_header_info(html: HTML):
    class QuoteSelectors(Base):
        name: str = ".D\(ib\).Fz\(18px\)"  # noqa: W605
        close: str = ".Trsdu\(0\.3s\).Fw\(b\).Fz\(36px\).Mb\(-4px\).D\(ib\)"  # noqa: W605
        change: str = ".Trsdu\(0\.3s\).Fw\(500\)"  # noqa: W605
        percent_change: str = ".Trsdu\(0\.3s\).Fw\(500\)"  # noqa: W605

    quote_header_info = html.find("div#quote-header-info", first=True)

    quote_data = {}

    if quote_header_info:

        for field, selector in QuoteSelectors():
            element = quote_header_info.find(selector)

            if element and len(element) == 1:
                quote_data[field] = element[0].text

    if quote_data:
        return Quote(**quote_data)
    else:
        return None
