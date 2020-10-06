# How to build a one delta OTM call options watchlist from twitter cashtags.

## Overview
1. First, we will scrape a users tweets for cashtags with [nitter_scraper](https://github.com/dgnsrekt/nitter_scraper/)
2. Next, we will prepare and clean the tweet data to build a watchlist.
3. After that, we will startup a network of tor nodes behind a reverse proxy, to bypass the yahoo finance rate limit, using [requests-whaor](https://github.com/dgnsrekt/requests-whaor/)
4. Last, we will download, clean, and concatenate all the options data into a single DataFrame.

## Requirements
* [Docker Engine](https://docs.docker.com/engine/) installed.
* python ^3.8
* [poetry](https://python-poetry.org/)

## Dependencies
* [yfs](https://github.com/dgnsrekt/yfs/)
* [nitter_scraper](https://github.com/dgnsrekt/nitter_scraper/)
* [requests-whaor](https://github.com/dgnsrekt/requests-whaor/)

!!! note
    requests-whaor will create multiple TOR nodes enclosed in docker containers to proxy your requests.

## Environment Preparation
Run the following commands to build a folder and initiate a poetry project.

```bash
$ mkdir yfs_watchlist
$ cd yfs_watchlist
$ poetry init
```
Keep hitting the enter button until you are out of the poetry init prompt.

Now lets add the dependencies.

```bash
$ poetry add nitter_scraper
$ poetry add git+https://github.com/dgnsrekt/requests-whaor.git@09c027dc7e27ab737ced95c2b7f18a6d862c78e7
$ poetry add yfs

```

Create options_bot.py

```bash
$ touch options_bot.py
```
Open options_bot.py in your favorite editor.

## Imports

```python
from concurrent.futures import as_completed, ThreadPoolExecutor
```
The ThreadPoolExecutor is used to call fuzzy_search and get_options_page functions asynchronously with a pool of threads.

```python
from nitter_scraper import NitterScraper
```
The nitter_scraper library is used to scrape tweets.

```python
import pandas
```
The pandas library is used to clean and concatenate the DataFrames.

```python
from requests import Session
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
```
The requests Session, HTTPAdapter and Retry objects are used to build a session which retries on failed requests.

```python
from requests_whaor import RequestsWhaor
```
The requests_whaor library will supply a rotating proxy server to send our requests through, giving each request a unique IP address.
If a request times out or gets a error code from the server it will retry with another IP address.

```python
from yfs import fuzzy_search, get_options_page
```
Last we use these yfs functions to search for valid symbols and get options data.


```python
from concurrent.futures import as_completed, ThreadPoolExecutor

from nitter_scraper import NitterScraper
import pandas
from requests import Session
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from requests_whaor import RequestsWhaor
from yfs import fuzzy_search, get_options_page
```

The imports should look like this.


## Scrape Twitter and build a watchlist

```python

watchlist = []
# Lets scrape the first page of eWhispers twitter feed for a list of symbols.
with NitterScraper(port=8008) as nitter:
    for tweet in nitter.get_tweets("eWhispers", pages=1):

        if tweet.is_pinned:  # Lets skip the pinned tweet.
            continue

        if tweet.is_retweet:  # Lets skip any retweets.
            continue

        if tweet.entries.cashtags:
            # Lets check if cashtags exists in the tweet then add them to the watchlist.
            watchlist += tweet.entries.cashtags

        print(".", end="", flush=True)  # Quick little progress bar so we don't get bored.
    print()  # Print a new line when complete just to make things look a little cleaner.


watchlist = sorted(set(map(lambda cashtag: cashtag.replace("$", "").strip(), watchlist)))
# Lets sort, remove duplicates, and clean '$' strings from each symbol.
```

Now we have a dynamically generated list of potentially interesting stock symbols.

```python
def get_session():
    session = Session()
    max_retries = Retry(
        total=20,
        connect=20,
        read=20,
        status_forcelist=[500, 502, 503, 504],
        respect_retry_after_header=False,
    )
    session.mount("http://", HTTPAdapter(max_retries=max_retries))
    session.mount("https://", HTTPAdapter(max_retries=max_retries))
    return session
```
Here we mount a Retry object on to the Session object.

!!! note
    [More details on the Retry object here.](https://urllib3.readthedocs.io/en/latest/reference/urllib3.util.html)

```python
valid_symbols = [] # Used to store symbols validated with the fuzzy_search function.
call_chains = [] # Used to store all the found call option chains.

# Decide on how many threads and proxies your computer can handle
MAX_THREADS = 6
# Each proxy is a tor circuit running inside a separate docker container.
MAX_PROXIES = 6
```

Now on to the meat of the code.

```python
with RequestsWhaor(onion_count=MAX_PROXIES, max_threads=MAX_THREADS) as request_whaor:
    # RequestsWhaor will spin up a network of TOR nodes we will use as a rotating proxy.

    with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
        futures = [
            executor.submit(
                fuzzy_search, ticker, proxies=request_whaor.rotating_proxy, session=get_session()
            )  # ^--Here we pass the rotating_proxy and session to the fuzzy_search function.
            for ticker in watchlist
        ]

        for future in as_completed(futures):
            result = future.result(timeout=60)

            print(".", end="", flush=True) #Quick progress bar.

            if result:
                # Now we append the results to the valid_symbols list.
                valid_symbols.append(result)  

        # Lets get the raw symbol from each ValidSymbol object.
        valid_symbols = [ticker.symbol for ticker in valid_symbols]

        print("found", len(valid_symbols)) # Number of valid symbols found.

        futures = [
            executor.submit(
                get_options_page,
                ticker,
                after_days=60,  # Lets get options that have at least 60 days before expiring.
                first_chain=True,  # We only want the first expiration with all strike prices.
                use_fuzzy_search=False,  # We did fuzzy search already no need to do it again.
                proxies=request_whaor.rotating_proxy,  # Pass the rotating_proxy.
                session=get_session(),  # Pass a session with a retry adapter.
                page_not_found_ok=True,  # return None if the symbol doesn't have an option page.
                timeout=5, # Pass a 5 second timeout to the session.
            )
            for ticker in valid_symbols
        ]

        for future in as_completed(futures):

            try:
                result = future.result(timeout=120)
                print(".", end="", flush=True) # Progress bar.

                if result:
                    if result.calls:
                        # If the results have a call option chain we will append it to the list.
                        call_chains.append(result.calls)

            except Exception as exc:
                # We will pass on any exceptions.
                print(exc)
```
!!! note
    [ThreadPoolExecutor information here.](https://docs.python.org/3/library/concurrent.futures.html)


## Final Section

* First, iterate over the result.
* Then, convert each chain into a dataframe.
* Next, get the first out of the money option and append it to a list.
* After that, concatenate the list of single option contract dataframes into a single dataframe.
* Now lets, drop some columns and sort by implied volatility to make things look pretty.
* Finally, print the results.

```python
first_otm_strike = []
for chain in call_chains:
    df = chain.dataframe
    otm = df[df["in_the_money"] == False].head(1)

    if otm is not None:
        first_otm_strike.append(otm)

final = pandas.concat(first_otm_strike, ignore_index=True)
final.drop(columns=["timestamp", "contract_name"], inplace=True)
final.sort_values(by="implied_volatility", inplace=True)
print(final.to_string())
```

Now we have a single dataframe of one delta OTM call options built from a dynamically generated watch list.

??? success "Output"
    ```bash

          symbol        contract_type  expiration_date  in_the_money  strike  last_price    bid    ask  change percent_change volume  open_interest  implied_volatility
    57    LMNR          call 2020-12-18 00:00:00+00:00         False    15.0        1.25   0.00   0.00    0.00           None      2            0.0                1.56
    101    SNX          call 2020-12-18 00:00:00+00:00         False   155.0        5.92   0.00   0.00    0.00            NaN      7           19.0                1.56
    99    SINA          call 2020-12-18 00:00:00+00:00         False    42.5        0.50   0.35   0.90    0.00            NaN      4          404.0               11.79
    41     GIS          call 2021-01-15 00:00:00+00:00         False    65.0        1.98   1.97   2.10   -0.29         -12.78     81         3192.0               23.22
    80     PEP          call 2020-12-18 00:00:00+00:00         False   140.0        4.50   4.60   4.85   -0.74         -14.12     31         4773.0               23.35
    25    COST          call 2021-01-15 00:00:00+00:00         False   360.0       19.50  18.80  19.70    1.32           7.26     55         3174.0               26.94
    21     CAG          call 2020-12-18 00:00:00+00:00         False    38.0        1.43   1.30   1.50   -0.04          -2.72      3            0.0               28.42
    49    INFO          call 2020-12-18 00:00:00+00:00         False    80.0        3.46   3.10   3.50    0.46          15.33      1          314.0               29.44
    68     MKC          call 2020-12-18 00:00:00+00:00         False   200.0        7.20   7.40   8.20    0.18           2.56      2          191.0               29.54
    2      ACN          call 2021-01-15 00:00:00+00:00         False   230.0       11.10  10.50  11.10   -0.70          -5.93      8          585.0               29.55
    96     RPM          call 2021-02-19 00:00:00+00:00         False    85.0        6.30   5.50   6.00    1.70          36.96      4           46.0               30.40
    55      KR          call 2021-01-15 00:00:00+00:00         False    35.0        2.00   1.96   2.05    0.10           5.26     87         1935.0               31.08
    76    ORCL          call 2020-12-18 00:00:00+00:00         False    60.0        3.10   3.05   3.20    0.05           1.64     26         1939.0               31.84
    79    PAYX          call 2020-12-18 00:00:00+00:00         False    82.5        3.90   3.90   4.40    0.90             30     36         1389.0               33.35
    102    STZ          call 2021-01-15 00:00:00+00:00         False   185.0       12.35  11.70  12.40   -1.99         -13.88     76          413.0               33.71
    17    CASY          call 2021-02-19 00:00:00+00:00         False   185.0       10.90  11.00  14.90    0.00            NaN    NaN            8.0               34.42
    73     NKE          call 2021-01-15 00:00:00+00:00         False   130.0        8.30   8.15   8.40    0.61           7.93    228         2868.0               34.64
    8      AZO          call 2020-12-18 00:00:00+00:00         False  1180.0       71.40  68.60  75.60    0.00            NaN      2           25.0               36.13
    37     FDS          call 2020-12-18 00:00:00+00:00         False   330.0       30.28  14.30  18.80    0.00            NaN     13           38.0               37.64
    26     COO          call 2020-12-18 00:00:00+00:00         False   350.0       12.00  15.50  20.40    0.00           None      5            8.0               38.32
    83    PRGS          call 2020-12-18 00:00:00+00:00         False    40.0        1.60   1.45   1.75   -0.30         -15.79      1          698.0               38.38
    44     HDS          call 2020-12-18 00:00:00+00:00         False    45.0        1.62   1.75   1.95    0.00            NaN     20          176.0               38.43
    15    CALM          call 2020-12-18 00:00:00+00:00         False    40.0        1.90   1.60   1.85    0.00            NaN     10           49.0               38.77
    27    CTAS          call 2020-12-18 00:00:00+00:00         False   340.0       19.75  17.70  22.00    0.00            NaN      2           14.0               39.15
    10    AVGO          call 2020-12-18 00:00:00+00:00         False   370.0       24.00  21.80  24.40    3.70          18.23     29          956.0               39.84
    32     DPZ          call 2020-12-18 00:00:00+00:00         False   430.0       27.50  27.00  29.10   -2.20          -7.41     50          119.0               41.16
    39     FUL          call 2021-02-19 00:00:00+00:00         False    50.0        4.00   2.10   3.90    0.00           None      1          126.0               41.46
    92     RGP          call 2021-02-19 00:00:00+00:00         False    15.0        0.30   0.10   0.30    0.10             50      1           19.0               41.90
    105   TCOM          call 2020-12-18 00:00:00+00:00         False    32.0        1.97   1.92   2.03   -0.09          -4.37     10         2958.0               42.14
    53     KMX          call 2021-01-15 00:00:00+00:00         False   100.0        7.89   7.60   8.00    1.39          21.38     84          609.0               43.25
    36     FDX          call 2021-01-15 00:00:00+00:00         False   260.0       23.20  22.35  23.70    1.07           4.84     92         1421.0               44.10
    115   VRNT          call 2020-12-18 00:00:00+00:00         False    50.0        2.63   3.40   3.80    0.00           None      1          855.0               44.69
    66     MTN          call 2020-12-18 00:00:00+00:00         False   230.0       11.50  11.90  14.70    0.00            NaN      1           75.0               44.95
    4      ABM          call 2021-01-15 00:00:00+00:00         False    40.0        2.45   1.95   2.30    0.00           None      1           83.0               45.41
    42    HELE          call 2020-12-18 00:00:00+00:00         False   210.0       12.00  12.60  15.90    1.00           9.09      1           51.0               46.17
    64      LW          call 2021-01-15 00:00:00+00:00         False    70.0        6.00   6.00   6.60    2.90          93.55      1          189.0               46.47
    3     ADBE          call 2020-12-18 00:00:00+00:00         False   490.0       38.65  38.05  39.55    0.15           0.39      3          168.0               47.17
    60     LEN          call 2021-01-15 00:00:00+00:00         False    85.0        7.30   7.10   7.40   -0.63          -7.94     17          800.0               47.29
    54     JBL          call 2020-12-18 00:00:00+00:00         False    36.0        1.83   2.40   2.75    0.00            NaN     10           21.0               47.41
    29    CVGW          call 2021-01-15 00:00:00+00:00         False    70.0        4.00   4.00   6.40    0.00           None    NaN            4.0               47.80
    69      MU          call 2021-01-15 00:00:00+00:00         False    50.0        3.80   3.80   3.85    0.30           8.57   1211        46526.0               48.32
    61    LULU          call 2020-12-18 00:00:00+00:00         False   340.0       28.30  28.75  29.30    0.30           1.07     62          680.0               49.95
    35     DRI          call 2021-01-15 00:00:00+00:00         False   105.0        9.75  10.00  10.60   -0.55          -5.34     42          808.0               51.20
    34    EPAC          call 2021-02-19 00:00:00+00:00         False    20.0        1.55   1.55   2.05    0.00           None    153          289.0               51.22
    20    CBRL          call 2020-12-18 00:00:00+00:00         False   120.0        8.40   7.90   9.50   -1.00         -10.64      3          141.0               51.43
    7     APOG          call 2021-02-19 00:00:00+00:00         False    25.0        1.44   1.80   2.10    0.00            NaN      3           45.0               51.56
    117     WB          call 2021-01-15 00:00:00+00:00         False    45.0        2.58   2.55   2.80    0.49          23.44     53         1539.0               51.93
    12     AYI          call 2020-12-18 00:00:00+00:00         False   110.0        9.20   7.80  10.30    2.10          29.58      1           72.0               52.27
    9     AVAV          call 2020-12-18 00:00:00+00:00         False    65.0        5.29   4.90   5.80    0.50          10.44     15           97.0               52.49
    94    SCHL          call 2020-12-18 00:00:00+00:00         False    22.5        1.45   1.45   1.85    0.00           None      5           13.0               52.83
    56    LEVI          call 2021-01-15 00:00:00+00:00         False    16.0        1.30   1.20   1.35    0.45          52.94     21          851.0               52.93
    112    WOR          call 2020-12-18 00:00:00+00:00         False    50.0        2.20   1.80   2.50    0.88          66.67    150          430.0               53.08
    74    NSSC          call 2020-12-18 00:00:00+00:00         False    25.0        1.20   0.80   2.75    0.00            NaN      3           51.0               53.08
    51     KBH          call 2021-01-15 00:00:00+00:00         False    40.0        4.25   4.20   4.30   -0.30          -6.59     27         1239.0               53.42
    18    CAMP          call 2020-12-18 00:00:00+00:00         False    10.0        0.20   0.05   0.25   -0.05            -20      9          552.0               55.47
    14     BRC          call 2021-05-21 00:00:00+00:00         False    45.0        3.40   3.00   6.30    0.00           None   None           32.0               56.12
    58    LNDC          call 2020-12-18 00:00:00+00:00         False    10.0        1.00   0.80   1.20   -0.45         -31.03      2           56.0               56.45
    23     CMD          call 2020-12-18 00:00:00+00:00         False    45.0        4.20   3.40   3.80    0.00           None      2           37.0               56.86
    11      BB          call 2020-12-18 00:00:00+00:00         False     5.0        0.27   0.26   0.30   -0.03            -10     33         1204.0               57.62
    78     OXM          call 2021-01-15 00:00:00+00:00         False    45.0        3.10   4.10   6.10    0.00            NaN     10           11.0               57.74
    72      NX          call 2020-12-18 00:00:00+00:00         False    20.0        1.50   0.90   1.70    0.00           None      1           18.0               57.81
    120     ZS          call 2021-01-15 00:00:00+00:00         False   150.0       15.40  15.25  16.30    0.80           5.48     71          626.0               58.11
    118   YEXT          call 2021-01-15 00:00:00+00:00         False    17.5        1.10   1.05   1.20    0.00            NaN      1          209.0               58.40
    119   ZUMZ          call 2021-02-19 00:00:00+00:00         False    30.0        3.22   3.50   3.80    0.00           None     30           50.0               59.08
    46     HQY          call 2020-12-18 00:00:00+00:00         False    55.0        4.33   4.20   4.90    0.00            NaN     10          185.0               59.16
    67    NEOG          call 2021-01-15 00:00:00+00:00         False    70.0        5.59   4.60   8.50    0.00           None      2            2.0               59.40
    75     NAV          call 2020-12-18 00:00:00+00:00         False    47.0        1.85   0.05   3.50    0.00           None   None            1.0               59.64
    6     ANGO          call 2021-01-15 00:00:00+00:00         False    12.5        1.30   1.00   1.45    0.00            NaN      4           32.0               59.67
    114    THO          call 2020-12-18 00:00:00+00:00         False   105.0        9.67  10.10  10.50    1.47          17.93      3           44.0               59.89
    33     EPM          call 2021-01-15 00:00:00+00:00         False     2.5        0.30   0.15   0.30    0.00           None      1           67.0               60.55
    98     SGH          call 2020-12-18 00:00:00+00:00         False    25.0        2.15   2.00   2.85   -0.50         -18.87     10            1.0               61.04
    81     PHR          call 2021-01-15 00:00:00+00:00         False    35.0        2.25   0.10   4.80    0.00           None      6           51.0               61.52
    24    COUP          call 2020-12-18 00:00:00+00:00         False   290.0       28.00  27.80  29.30    1.40           5.26      5          112.0               62.32
    22    CMTL          call 2021-01-15 00:00:00+00:00         False    17.5        1.40   1.25   1.45    0.65          86.67     18          307.0               63.28
    77      NG          call 2020-12-18 00:00:00+00:00         False    12.0        0.90   0.85   1.00   -0.02          -2.17      3         1171.0               63.28
    91      RH          call 2021-01-15 00:00:00+00:00         False   380.0       49.70  48.70  51.60   -3.30          -6.23     13          357.0               63.32
    90    RFIL          call 2021-01-15 00:00:00+00:00         False     5.0        0.45   0.30   0.50    0.00           None      3          131.0               63.48
    103   SLQT          call 2021-01-15 00:00:00+00:00         False    22.5        2.50   1.80   2.10    0.05           2.04    100           90.0               63.77
    95    SCWX          call 2021-01-15 00:00:00+00:00         False    12.5        1.40   1.05   1.30    0.00           None     40           87.0               63.87
    116   WORK          call 2020-12-18 00:00:00+00:00         False    30.0        2.60   2.53   2.62    0.26          11.11    320         8619.0               64.55
    19    CHWY          call 2021-01-15 00:00:00+00:00         False    60.0        6.94   6.90   7.10    0.34           5.15    231         3165.0               66.36
    5      AEO          call 2021-01-15 00:00:00+00:00         False    16.0        1.90   1.80   2.10    0.00            NaN     12          270.0               66.94
    113   UNFI          call 2021-02-19 00:00:00+00:00         False    17.5        2.50   2.50   2.65    0.20            8.7     51          600.0               67.19
    62    MDLA          call 2020-12-18 00:00:00+00:00         False    30.0        2.53   2.40   2.80    0.28          12.44      6          574.0               67.19
    31    DOCU          call 2020-12-18 00:00:00+00:00         False   230.0       25.10  24.50  26.40    3.31          15.19    269         1010.0               67.27
    108   TLYS          call 2020-12-18 00:00:00+00:00         False     6.5        0.85   0.60   0.95   -1.05         -55.26      8          134.0               68.56
    111   VITL          call 2021-01-15 00:00:00+00:00         False    40.0        7.00   4.50   6.70    0.00            NaN      3           10.0               69.39
    63    MCFT          call 2021-01-15 00:00:00+00:00         False    20.0        2.95   2.45   3.30    0.70          31.11      1           16.0               71.53
    87    REVG          call 2021-01-15 00:00:00+00:00         False    10.0        0.50   0.50   0.95    0.00            NaN      5           43.0               72.17
    70    NCNO          call 2021-02-19 00:00:00+00:00         False    80.0       12.90  11.60  12.10    0.00            NaN      1           19.0               73.83
    100   SFIX          call 2020-12-18 00:00:00+00:00         False    29.0        3.75   3.60   4.05    0.66          21.36     22          198.0               76.95
    48    ICMB          call 2021-01-15 00:00:00+00:00         False     5.0        0.20   0.00   0.35    0.00           None     30          126.0               77.73
    107   UEPS          call 2021-01-15 00:00:00+00:00         False     4.0        0.35   0.25   0.50    0.05          16.67     10          253.0               77.73
    47     HMY          call 2021-01-15 00:00:00+00:00         False     6.0        0.70   0.60   0.75    0.04           6.06     33         1786.0               78.81
    30    DOMO          call 2021-02-19 00:00:00+00:00         False    38.0        7.18   6.60   7.20    0.00            NaN      1           15.0               79.44
    52    LAKE          call 2021-01-15 00:00:00+00:00         False    22.5        3.29   3.40   3.80    0.39          13.45     10          208.0               79.61
    104    TNP          call 2020-12-18 00:00:00+00:00         False    10.0        0.55   0.50   0.70    0.10          22.22      4          265.0               80.18
    86    PTON          call 2021-01-15 00:00:00+00:00         False   115.0       16.70  16.20  18.00    1.40           9.15    174          705.0               81.09
    88     RAD          call 2021-01-15 00:00:00+00:00         False    10.0        1.53   1.53   1.60   -0.12          -7.27     71         1218.0               81.93
    13    BBBY          call 2020-12-18 00:00:00+00:00         False    21.0        2.86   2.75   2.83   -0.12          -4.03     80         4088.0               81.98
    50     JKS          call 2020-12-18 00:00:00+00:00         False    50.0        6.00   5.90   6.90    1.60          36.36     16           51.0               82.10
    0     AGTC          call 2021-01-15 00:00:00+00:00         False     7.5        0.35   0.30   0.45    0.00            NaN     70         2883.0               82.23
    38     FLR          call 2021-01-15 00:00:00+00:00         False    10.0        1.70   1.60   1.75    0.15           9.68    116         5774.0               88.18
    45    GIII          call 2020-12-18 00:00:00+00:00         False    15.0        1.85   2.20   2.45    0.00            NaN      5         1146.0               91.60
    59    LOVE          call 2021-01-15 00:00:00+00:00         False    30.0        5.61   5.50   5.90    0.00            NaN      1           34.0               92.99
    106   SWBI          call 2020-12-18 00:00:00+00:00         False    17.5        2.80   2.75   3.00    0.20           7.69     58          849.0               96.44
    16    BIGC          call 2021-01-15 00:00:00+00:00         False    95.0       18.80  18.00  18.90    3.45          22.48      8           81.0              101.03
    28    DLNG          call 2021-01-15 00:00:00+00:00         False     2.5        0.45   0.30   0.65    0.00           None    418          719.0              102.73
    93    SANW          call 2021-02-19 00:00:00+00:00         False     2.5        1.11   0.50   0.65    0.00           None     12            6.0              105.08
    85     QTT          call 2021-01-15 00:00:00+00:00         False     2.5        0.55   0.10   0.70    0.00            NaN      1          100.0              106.64
    89    RLGT          call 2020-12-18 00:00:00+00:00         False     7.5        0.10   0.00   0.80    0.00           None      2           17.0              109.77
    82    PLAY          call 2021-01-15 00:00:00+00:00         False    17.5        2.55   2.30   3.30   -0.20          -7.27     32         1737.0              110.16
    71    NTWK          call 2021-01-15 00:00:00+00:00         False     5.0        0.05   0.00   0.50    0.00           None      5           63.0              111.33
    1      ACB          call 2020-12-18 00:00:00+00:00         False     5.0        0.77   0.75   0.81    0.07             10     91          998.0              112.11
    65    MEIP          call 2020-12-18 00:00:00+00:00         False     5.0        0.21   0.20   0.25    0.11            110      3        12695.0              115.23
    84      QD          call 2021-01-15 00:00:00+00:00         False     1.5        0.25   0.15   0.35    0.00            NaN      5          350.0              117.19
    43     GME          call 2021-01-15 00:00:00+00:00         False    10.0        2.27   2.30   2.40   -0.02          -0.87   1520        15764.0              129.79
    40    FCEL          call 2021-01-15 00:00:00+00:00         False     2.0        0.58   0.57   0.59   -0.02          -3.33    765         4591.0              158.98
    110   UXIN          call 2021-01-15 00:00:00+00:00         False     1.0        0.30   0.25   0.35    0.00           None      2          752.0              164.06
    97    SEAC          call 2021-01-15 00:00:00+00:00         False     2.5        0.05   0.05   0.15    0.00           None      4         1760.0              189.84
    109   USAT          call 2021-01-15 00:00:00+00:00         False    10.0        1.25   0.70   9.80    0.00           None      2           41.0              351.17
    ```

## Full Script

```python
from concurrent.futures import as_completed, ThreadPoolExecutor

from nitter_scraper import NitterScraper
import pandas
from requests import Session
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from requests_whaor import RequestsWhaor
from yfs import fuzzy_search, get_options_page

watchlist = []
# Lets scrape the first page of eWhispers twitter feed for a list of symbols.
with NitterScraper(port=8008) as nitter:
    for tweet in nitter.get_tweets("eWhispers", pages=1):

        if tweet.is_pinned:  # Lets skip the pinned tweet.
            continue

        if tweet.is_retweet:  # Lets skip any retweets.
            continue

        if tweet.entries.cashtags:
            # Lets check if cashtags exists in the tweet then add them to the watchlist.
            watchlist += tweet.entries.cashtags

        print(".", end="", flush=True)  # Quick little progress_bar so we don't get bored.
    print()  # Print new line when complete just to make things look a little cleaner.


watchlist = sorted(set(map(lambda cashtag: cashtag.replace("$", "").strip(), watchlist)))
# Lets sort, remove duplicates, and clean '$' strings from each symbols.

def get_session():
    session = Session()
    max_retries = Retry(
        total=20,
        connect=20,
        read=20,
        status_forcelist=[500, 502, 503, 504],
        respect_retry_after_header=False,
    )
    session.mount("http://", HTTPAdapter(max_retries=max_retries))
    session.mount("https://", HTTPAdapter(max_retries=max_retries))
    return session

valid_symbols = [] # Used to store symbols validated with the fuzzy_search function.
call_chains = [] # Used to store all the found call option chains.

# Decide on how many threads and proxies your computer can handle
MAX_THREADS = 6
# Each proxy is a tor circuit running inside a separate docker container.
MAX_PROXIES = 6

with RequestsWhaor(onion_count=MAX_PROXIES, max_threads=MAX_THREADS) as request_whaor:
    # RequestsWhaor will spin up a network of TOR nodes we will use as a rotating proxy.

    with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
        futures = [
            executor.submit(
                fuzzy_search, ticker, proxies=request_whaor.rotating_proxy, session=get_session()
            )  # ^--Here we pass the rotating_proxy and session to the fuzzy_search function.
            for ticker in watchlist
        ]

        for future in as_completed(futures):
            result = future.result(timeout=60)

            print(".", end="", flush=True) #Quick progress bar.

            if result:
                # Now we append the results to the valid_symbols list.
                valid_symbols.append(result)  

        # Lets get the raw symbol from each ValidSymbol object.
        valid_symbols = [ticker.symbol for ticker in valid_symbols]

        print("found", len(valid_symbols)) # Number of valid symbols found.

        futures = [
            executor.submit(
                get_options_page,
                ticker,
                after_days=60,  # Lets get options that have at least 60 days before expiring.
                first_chain=True,  # We only want the first expiration with all strike prices.
                use_fuzzy_search=False,  # We did fuzzy search already no need to do it again.
                proxies=request_whaor.rotating_proxy,  # Pass the rotating_proxy.
                session=get_session(),  # Pass a session with a retry adapter.
                page_not_found_ok=True,  # return None if the symbol doesn't have an option page.
                timeout=5, # Pass a 5 second timeout to the session.
            )
            for ticker in valid_symbols
        ]

        for future in as_completed(futures):

            try:
                result = future.result(timeout=120)
                print(".", end="", flush=True) # Progress bar.

                if result:
                    if result.calls:
                        # If the results have a call option chain we will append it to the list.
                        call_chains.append(result.calls)

            except Exception as exc:
                # We will pass on any exceptions.
                print(exc)

first_otm_strike = []

for chain in call_chains:
    df = chain.dataframe
    otm = df[df["in_the_money"] == False].head(1)

    if otm is not None:
        first_otm_strike.append(otm)

final = pandas.concat(first_otm_strike, ignore_index=True)
final.drop(columns=["timestamp", "contract_name"], inplace=True)
final.sort_values(by="implied_volatility", inplace=True)
print(final.to_string())    
```
