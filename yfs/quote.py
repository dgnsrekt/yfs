from typing import Optional

from pydantic import BaseModel as Base
from pydantic import validator as clean
from requests_html import HTML

from .cleaner import CommonCleaners, cleaner


def clean_quote_name(cls, value):
    value = value.split("(")
    return value[0].strip()


class Quote(Base):
    name: str
    close: Optional[float]
    change: Optional[float]
    percent_change: Optional[float]

    _clean_name = cleaner("name")(clean_quote_name)

    _clean_close = cleaner("close")(CommonCleaners.clean_common_values)

    _clean_change = cleaner("change")(CommonCleaners.clean_first_value_split_by_space)

    _clean_percent_change = cleaner("percent_change")(
        CommonCleaners.clean_second_value_split_by_space
    )


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
