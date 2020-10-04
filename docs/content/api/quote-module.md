> Module for parsing quote header data from a yahoo finance page.

<a name="quote.clean_quote_name"></a>
#### `clean_quote_name`

```python
def clean_quote_name(value: str) -> str
```

> Remove the symbol and strip whitespace from the company name.
> 
> **Arguments**:
> 
> - `value` _str_ - A company name string parsed from the quote hearder
>   portion of any yahoo finance page.
>   
> 
> **Example**:
> 
>   |Input             |Output    |
>   |------------------|----------|
>   |Apple Inc. (AAPL) |Apple Inc.|
>   
> 
> **Returns**:
> 
> - `str` - Company name with the ticker symbol removed.

<a name="quote.Quote"></a>
## `Quote`

> Represents all the data parsed from the quote header section of a yahoo finance page.
> 
> **Attributes**:
> 
> - `name` _str_ - Company name.
> - `close` _float_ - Close price.
> - `change` _float_ - Dollar change in price.
> - `percent_change` _float_ - Percent change in price.
>   
> 
> **Notes**:
> 
>   This class inherits from the pydantic BaseModel which allows for the use
>   of .json() and .dict() for serialization to json strings and dictionaries.
>   
> - `.json()` - Serialize to a JSON object.
> - `.dict()` - Serialize to a dictionary.

<a name="quote.parse_quote_header_info"></a>
#### `parse_quote_header_info`

```python
def parse_quote_header_info(html: HTML) -> Optional[Quote]
```

> Parse and clean html elements from the quote header info portion of a yahoo finance page.
> 
> **Arguments**:
> 
> - `html` _HTML_ - An HTML object contaning quote header info data ready to be parse.
>   
> 
> **Returns**:
> 
> - `Quote` - Quote object contaning the parsed quote header data if successfully parsed.
> - `None` - No quote header info data present in the HTML.

