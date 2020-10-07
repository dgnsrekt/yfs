"""Module for parsing quote header data from a yahoo finance page."""

from typing import Optional

from pydantic import BaseModel as Base
from requests_html import HTML

from .cleaner import cleaner, CommonCleaners


def clean_quote_name(value: str) -> str:
    """Remove the symbol and strip whitespace from the company name.

    Args:
        value (str): A company name string parsed from the quote header
            portion of any yahoo finance page.

    Example:
        |Input             |Output    |
        |------------------|----------|
        |Apple Inc. (AAPL) |Apple Inc.|

    Returns:
        str: Company name with the ticker symbol removed.

    """
    value = value.split("(")
    return value[0].strip()


class Quote(Base):
    """Represents all the data parsed from the quote header section of a yahoo finance page.

    Attributes:
        name (str): Company name.
        close (float): Close price.
        change (float): Dollar change in price.
        percent_change (float): Percent change in price.

    Notes:
        This class inherits from the pydantic BaseModel which allows for the use
        of .json() and .dict() for serialization to json strings and dictionaries.

        .json(): Serialize to a JSON object.
        .dict(): Serialize to a dictionary.
    """

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


def parse_quote_header_info(html: HTML) -> Optional[Quote]:
    """Parse and clean html elements from the quote header info portion of a yahoo finance page.

    Args:
        html (HTML): An HTML object containing quote header info data ready to be parse.

    Returns:
        Quote: Quote object containing the parsed quote header data if successfully parsed.
        None: No quote header info data present in the HTML.
    """
    quote_selectors = {
        "name": r".D\(ib\).Fz\(18px\)",
        "close": r".Trsdu\(0\.3s\).Fw\(b\).Fz\(36px\).Mb\(-4px\).D\(ib\)",
        "change": r".Trsdu\(0\.3s\).Fw\(500\)",
        "percent_change": r".Trsdu\(0\.3s\).Fw\(500\)",
    }

    quote_header_info = html.find("div#quote-header-info", first=True)

    quote_data = {}

    if quote_header_info:

        for field, selector in quote_selectors.items():
            element = quote_header_info.find(selector)

            if element and len(element) == 1:
                quote_data[field] = element[0].text

    if quote_data:
        return Quote(**quote_data)

    return None
