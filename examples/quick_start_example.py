from yfs import get_multiple_summary_pages

search_items = ["Apple", "tsla", "Microsoft", "AMZN"]

summary_results = get_multiple_summary_pages(search_items)
for page in summary_results:
    print(page.json(indent=4))
    break  # To shorten up the quick-start output.

COLUMNS = [
    "close",
    "change",
    "percent_change",
    "average_volume",
    "market_cap",
    "earnings_date",
]
print(summary_results.dataframe[COLUMNS])

"""
➜ python3 quick_start_example.py
Downloading Summary Data... 100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 4/4 [00:03<00:00, 1.19 symbols/s]{
    "symbol": "AAPL",
    "name": "Apple Inc.",
    "quote": {
        "name": "Apple Inc.",
        "close": 113.02,
        "change": -3.77,
        "percent_change": -3.23
    },
    "open": 112.89,
    "high": 112.22,
    "low": 115.37,
    "close": 113.02,
    "change": -3.77,
    "percent_change": -3.23,
    "previous_close": 116.79,
    "bid_price": 112.58,
    "bid_size": 800,
    "ask_price": 112.77,
    "ask_size": 3000,
    "fifty_two_week_low": 137.98,
    "fifty_two_week_high": 53.15,
    "volume": 144711986,
    "average_volume": 172065562,
    "market_cap": 1933000000000,
    "beta_five_year_monthly": 1.28,
    "pe_ratio_ttm": 34.29,
    "eps_ttm": 3.3,
    "earnings_date": "2020-10-28",
    "forward_dividend_yield": 0.82,
    "forward_dividend_yield_percentage": 0.7,
    "exdividend_date": "2020-08-07",
    "one_year_target_est": 119.24
}
          close  change  percent_change  average_volume     market_cap earnings_date
symbol
AAPL     113.02   -3.77           -3.23       172065562  1933000000000    2020-10-28
AMZN    3125.00  -96.26           -2.99         5071692  1565000000000    2020-10-29
MSFT     206.19   -6.27           -2.95        34844893  1560000000000    2020-10-21
TSLA     415.09  -33.07           -7.38        80574089   386785000000    2020-10-21
"""
