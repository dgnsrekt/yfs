> A module for cleaning tables, fields and values.

<a name="cleaner.field_cleaner"></a>
#### `field_cleaner`

```python
def field_cleaner(field: str) -> str
```

> Convert field string from an html response into a snake case variable.
> 
> **Arguments**:
> 
> - `field` _str_ - A dirty field string.
>   
> 
> **Example**:
> 
>   |Input             |  Output                |
>   |------------------|------------------------|
>   |Previous Close    | previous_close         |
>   |Avg. Volume       | avg_volume             |
>   |Beta (5Y Monthly) | beta_five_year_monthly |
>   |PE Ratio (TTM)    | pe_ratio_ttm           |
>   
> 
> **Returns**:
> 
> - `str` - lowercased and converted to snake case.

<a name="cleaner.table_cleaner"></a>
#### `table_cleaner`

```python
def table_cleaner(html_table: HTML) -> Optional[Dict]
```

> Clean table with two fields.
> 
> **Arguments**:
> 
> - `html_table` _HTML_ - HTML object parsed from a table section.
>   
> 
> **Returns**:
> 
> - `dict` - cleaned fields (keys) and string (values).
> - `None` - if html_table does not contain table elements.

<a name="cleaner.cleaner"></a>
#### `cleaner`

> * Partial overloading the pytdanitc.validator function with common args.

<a name="cleaner.CommonCleaners"></a>
## `CommonCleaners`

> Contains the most commonly used methods for cleaning values.

<a name="cleaner.CommonCleaners.remove_comma"></a>
#### `remove_comma`

```python
 | def remove_comma(value: str) -> str
```

> Remove commas from strings and strip whitespace.
> 
> **Arguments**:
> 
> - `value` _str_ - A number with more than 3 digits.
>   
> 
> **Example**:
> 
>   |Input   | Output|
>   |--------|-------|
>   |'5,000' | '5000'|
>   
> 
> **Returns**:
> 
> - `str` - Commas removed and whitespace stripped.

<a name="cleaner.CommonCleaners.remove_brakets"></a>
#### `remove_brakets`

```python
 | def remove_brakets(value: str) -> str
```

> Remove () brakets from strings and strip whitespace.
> 
> **Arguments**:
> 
> - `value` _str_ - Containing () brakets. Normally surrounding a percent change.
>   
> 
> **Example**:
> 
>   |Input           |Output       |
>   |----------------|-------------|
>   |+19.60 (+1.36%) |+19.60 +1.36 |
>   
> 
> **Returns**:
> 
> - `str` - () brakets removed and whitespace stripped.

<a name="cleaner.CommonCleaners.remove_percent_sign"></a>
#### `remove_percent_sign`

```python
 | def remove_percent_sign(value: str) -> str
```

> Remove percent sign % from string and strip whitespace.
> 
> **Arguments**:
> 
> - `value` _str_ - Containing percent sign.
>   
> 
> **Example**:
> 
>   |Input     |Output |
>   |----------|-------|
>   |+1.36%    |+1.36  |
>   
> 
> **Returns**:
> 
> - `str` - Percent sign % removed and whitespace stripped.

<a name="cleaner.CommonCleaners.remove_brakets_and_percent_sign"></a>
#### `remove_brakets_and_percent_sign`

```python
 | def remove_brakets_and_percent_sign(cls, value: str) -> str
```

> Remove () brakets and % percent signs from string.
> 
> **Arguments**:
> 
> - `value` _str_ - Contains () backets and % percent sign.
>   
> 
> **Example**:
> 
>   |Input              |Output      |
>   |-------------------|------------|
>   |+19.60 (+1.36%)    |+19.60 +1.36|
>   
> 
> **Returns**:
> 
> - `str` - () brakets % percent sign removed.

<a name="cleaner.CommonCleaners.value_is_missing"></a>
#### `value_is_missing`

```python
 | def value_is_missing(value: str) -> bool
```

> Check if value has missing data.
> 
> It checks to see if "N/A" and other missing data strings are present in the value.
> 
> **Arguments**:
> 
> - `value` _str_ - A value parsed from yahoo finance.
>   
> 
> **Example**:
> 
>   |Input                    |Output      |
>   |-------------------------|------------|
>   |"Ex-Dividend Date    N/A"|True        |
>   
> 
> **Returns**:
> 
> - `bool` - True if a missing data string is found in value else False.

<a name="cleaner.CommonCleaners.has_large_number_suffix"></a>
#### `has_large_number_suffix`

```python
 | def has_large_number_suffix(value: str) -> bool
```

> Check if string representation of a number has T,B,M,K suffix.
> 
> **Arguments**:
> 
> - `value` _str_ - A value to check if contains a T,B,M,K suffix.
>   
> 
> **Example**:
> 
>   
>   |Input  |Output      |
>   |-------|------------|
>   |225.0M |True        |
>   
> 
> **Returns**:
> 
> - `bool` - True if string value contains T,B,M,K suffix else false.

<a name="cleaner.CommonCleaners.clean_large_number"></a>
#### `clean_large_number`

```python
 | def clean_large_number(value: str) -> Optional[int]
```

> Convert a string representation of a number with a T,B,M,K suffix to an int.
> 
> **Arguments**:
> 
> - `value` _str_ - A value which contains T,B,M,K suffix.
>   
> 
> **Example**:
> 
>   |Input |Output       |
>   |------|-------------|
>   |2.5B  |2_500_000_000|
>   
> 
> **Returns**:
> 
> - `int` - suffix removed and used as multiplier to convert to an int.
> - `None` - This can return None, but should not because the
>   has_large_number_suffix method should be used to check if
>   this method should even be run.

<a name="cleaner.CommonCleaners.common_value_cleaner"></a>
#### `common_value_cleaner`

```python
 | def common_value_cleaner(cls, value: str) -> Union[int, str]
```

> Most common method for cleaning most values from yahoo finance.
> 
> Removes commas and converts number if it has a suffix.
> 
> **Arguments**:
> 
> - `value` _str_ - value to be cleaned.
>   
> 
> **Example**:
> 
>   |Input   |Output       |Type|
>   |--------|-------------|----|
>   |"5,000" | "5000"      |str |
>   |"2.5M"  | 2_500_000   |int |
>   
> 
> **Returns**:
> 
> - `str` - If value is cleaned and doesn't have a suffix.
> - `int` - If value is cleaned and has a suffix.

<a name="cleaner.CommonCleaners.clean_common_values"></a>
#### `clean_common_values`

```python
 | def clean_common_values(cls, value: str) -> Optional[Union[int, str]]
```

> Most common vanilla method for cleaning most values with a check for missing values.
> 
> **Arguments**:
> 
> - `value` _str_ - value to be cleaned.
>   
> 
> **Example**:
> 
>   |Input      |Output    |Type|
>   |-----------|----------|----|
>   |"5,000"    |"5000"    |str |
>   |"2.5M"     |2_500_000 |int |
>   |"N/A"      |None      |None|
>   
> 
> **Returns**:
> 
> - `str` - If value is cleaned and doesn't have a suffix.
> - `int` - If value is cleaned and has a suffix.
> - `None` - If value is missing.

<a name="cleaner.CommonCleaners.clean_basic_percentage"></a>
#### `clean_basic_percentage`

```python
 | def clean_basic_percentage(cls, value: str) -> Optional[str]
```

> Clean a single percentage value.
> 
> **Arguments**:
> 
> - `value` _str_ - value to be cleaned.
>   
> 
> **Example**:
> 
>   |Input   |Output |Type|
>   |--------|-------|----|
>   |"-3.4%" |"-3.4" |str |
>   |"N/A"   |None   |None|
>   
> 
> **Returns**:
> 
> - `str` - cleaned value if value is not missing.
> - `None` - if value is missing.

<a name="cleaner.CommonCleaners.clean_date"></a>
#### `clean_date`

```python
 | def clean_date(cls, value: str) -> DateTime
```

> Clean and convert a string date.
> 
> Uses pendulum parse method to extract datetime information. Sometimes yahoo
> finance give multiple dates in one value field. This normally happens in the
> Earnings Date section on the Summary page. The Earnings Date may have a single
> date or an estimated Earnings Date range. It would be very easy to have this method
> output a pendulum.period.Period object that can represent the date range. The
> decision was made to just return the start of the earnings period for consistency.
> 
> **Arguments**:
> 
> - `value` _str_ - Date string to be converted to datetime object.
>   
> 
> **Example**:
> 
>   |Input                                         |Output                            |
>   |----------------------------------------------|----------------------------------|
>   |"Earnings Date    Oct 26, 2020 - Oct 30, 2020"|DateTime 2020-10-26T00:00:00+00:00|
>   
> 
> **Returns**:
> 
> - `str` - cleaned if value is not missing.
> - `None` - if value is missing.

<a name="cleaner.CommonCleaners.clean_symbol"></a>
#### `clean_symbol`

```python
 | def clean_symbol(cls, value: str) -> str
```

> Make symbol uppercase.
> 
> **Arguments**:
> 
> - `value` _str_ - Stock symbol.
>   
> 
> **Example**:
> 
>   |Input |Output |
>   |------|-------|
>   |aapl  |AAPL   |
>   
> 
> **Returns**:
> 
> - `str` - Uppercased.

<a name="cleaner.CommonCleaners.clean_first_value_split_by_dash"></a>
#### `clean_first_value_split_by_dash`

```python
 | def clean_first_value_split_by_dash(cls, value: str) -> str
```

> Split value separated by '-' and return the first value.
> 
> **Arguments**:
> 
> - `value` _str_ - A string with multiple values separated by a '-'.
>   
> 
> **Example**:
> 
>   |Input            |Output  |
>   |-----------------|--------|
>   |"2.3400 - 2.4900"|"2.3400"|
>   
> 
> **Returns**:
> 
> - `strs` - First value parse from string.
> - `None` - if value is missing.

<a name="cleaner.CommonCleaners.clean_second_value_split_by_dash"></a>
#### `clean_second_value_split_by_dash`

```python
 | def clean_second_value_split_by_dash(cls, value: str) -> str
```

> Split value separated by '-' and return the second value.
> 
> **Arguments**:
> 
> - `value` _str_ - A string with multiple values separated by a '-'.
>   
> 
> **Example**:
> 
>   |Input            |Output  |
>   |-----------------|--------|
>   |"2.3400 - 2.4900"|"2.4900"|
>   
> 
> **Returns**:
> 
> - `strs` - Second value parse from string.
> - `None` - if value is missing.

<a name="cleaner.CommonCleaners.clean_first_value_split_by_space"></a>
#### `clean_first_value_split_by_space`

```python
 | def clean_first_value_split_by_space(cls, value: str) -> str
```

> Clean first string containing a change and percent.
> 
> This will strip brakets and percent sign leaving only a whitespace
> between the change and percent change. Next it will split the values then
> return the first value. Normally the Forward Dividend & Yield from the
> summary page.
> 
> **Arguments**:
> 
> - `value` _str_ - Normally a string containing change and percent change.
>   
> 
> **Example**:
> 
>   |Input            |Output  |
>   |-----------------|--------|
>   |"0.82 (0.73%)"   |"0.82"  |
>   
> 
> **Returns**:
> 
> - `str` - The first string.
> - `None` - if value is missing.

<a name="cleaner.CommonCleaners.clean_second_value_split_by_space"></a>
#### `clean_second_value_split_by_space`

```python
 | def clean_second_value_split_by_space(cls, value: str) -> str
```

> Clean second string containing a change and percent.
> 
> This will strip brakets and percent sign leaving only a whitespace
> between the change and percent change. Next it will split the values then
> return the second value. Normally the Forward Dividend & Yield from the
> summary page.
> 
> **Arguments**:
> 
> - `value` _str_ - Normally a string containing change and percent change.
>   
> 
> **Example**:
> 
>   |Input            |Output  |
>   |-----------------|--------|
>   |"0.82 (0.73%)"   |"0.73"  |
>   
> 
> **Returns**:
> 
> - `str` - The Second value.
> - `None` - if value is missing.

<a name="cleaner.CommonCleaners.clean_first_value_split_by_x"></a>
#### `clean_first_value_split_by_x`

```python
 | def clean_first_value_split_by_x(cls, value: str) -> str
```

> Split value separated by 'x' and return the first value.
> 
> **Arguments**:
> 
> - `value` _str_ - A string with multiple values separated by a 'x'.
>   
> 
> **Example**:
> 
>   |Input            |Output  |
>   |-----------------|--------|
>   |"2.4000 x 21500" |"2.4000"|
>   
> 
> **Returns**:
> 
> - `strs` - First value parse from string.
> - `None` - if value is missing.

<a name="cleaner.CommonCleaners.clean_second_value_split_by_x"></a>
#### `clean_second_value_split_by_x`

```python
 | def clean_second_value_split_by_x(cls, value: str) -> str
```

> Split value separated by 'x' and return the second value.
> 
> **Arguments**:
> 
> - `value` _str_ - A string with multiple values separated by a 'x'.
>   
> 
> **Example**:
> 
>   |Input            |Output  |
>   |-----------------|--------|
>   |"2.4000 x 21500" |"21500" |
>   
> 
> **Returns**:
> 
> - `strs` - Second value parse from string.
> - `None` - if value is missing.

