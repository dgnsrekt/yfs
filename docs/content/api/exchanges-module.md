> Module for exchanges organized by region.

<a name="exchanges.UnitedStatesExchanges"></a>
## `UnitedStatesExchanges`

> Exchanges based out of the United States.

<a name="exchanges.CanadianExchanges"></a>
## `CanadianExchanges`

> Exchanges Based out of Canda.

<a name="exchanges.SouthAmericanExchanges"></a>
## `SouthAmericanExchanges`

> Exchanges Based out of South America.

<a name="exchanges.EuropeanExchanges"></a>
## `EuropeanExchanges`

> Exchanges Based out of Europe.

<a name="exchanges.AfricanExchanges"></a>
## `AfricanExchanges`

> Exchanges Based out of Africa.

<a name="exchanges.MiddleEasternExchanges"></a>
## `MiddleEasternExchanges`

> Exchanges Based out of MiddleEast.

<a name="exchanges.AsianExchanges"></a>
## `AsianExchanges`

> Exchanges Based out of Asia.

<a name="exchanges.AustralianExchanges"></a>
## `AustralianExchanges`

> Exchanges Based out of Australia.

<a name="exchanges.UnknownExchanges"></a>
## `UnknownExchanges`

> Exchanges that haven't been identified yet.

<a name="exchanges.ExchangeTypes"></a>
## `ExchangeTypes`

> Helper for choosing a valid exchange region.
> 
> This is used for filtering out results from a fuzzy_search request.
> 
> **Attributes**:
> 
> - `united_states` _Enum_ - UnitedStatesExchanges
> - `canada` _Enum_ - CanadianExchanges
> - `australian` _Enum_ - AustralianExchanges
> - `asia` _Enum_ - AsianExchanges
> - `south_america` _Enum_ - SouthAmericanExchanges
> - `europe` _Enum_ - EuropeanExchanges
> - `middle_east` _Enum_ - MiddleEasternExchanges
> - `africa` _Enum_ - AfricanExchanges
> - `unknown` _Enum_ - UnknownExchanges

<a name="exchanges.ExchangeTypes.show"></a>
#### `show`

```python
 | def show(cls) -> None
```

> Print out all valid exchanges.

