from nitter_scraper import NitterScraper
from yfs.symbol import fuzzy_symbol_seach
from yfs.summary import get_summary_page, get_summary_pages
from requests.exceptions import ConnectionError, ProxyError, Timeout, RequestException
import requests
from requests import Session
from concurrent.futures import as_completed, ThreadPoolExecutor
import enlighten
from more_itertools import chunked
from requests_whaor import RequestsWhaor


def get(cashtag, proxies):

    try:
        results = get_summary_page(cashtag, proxies=proxies, timeout=5)
        return results

    except RequestException as e:
        print(e)
        print("trying again.")
        get(cashtag, proxies)


user = "eWhispers"
with RequestsWhaor(onion_count=5) as requests_whaor:
    with NitterScraper(host="0.0.0.0", port=8008) as nitter:
        for idx, tweet in enumerate(nitter.get_tweets(user, pages=100)):
            cashtags = [cashtag.replace("$", "") for cashtag in tweet.entries.cashtags]
            cashtags = sorted(set(cashtags))
            if len(cashtags) > 0:
                results = get_summary_pages(
                    cashtags, proxies=requests_whaor.proxies, with_threads=True, thread_count=5
                )

                if results:
                    print(results.dataframe)

            if idx % 100 == 0:
                requests_whaor.restart_onions()

# with NitterScraper(host="0.0.0.0", port=8008) as nitter:
#     for idx, tweet in enumerate(nitter.get_tweets(user, pages=100)):
#         cashtags += [cashtag.replace("$", "") for cashtag in tweet.entries.cashtags]
#         cashtags = sorted(set(cashtags))
#         if len(cashtags) > 0:
#             print(idx, len(cashtags), cashtags[0], cashtags[-1])
#
#
# with RequestsWhaor(onion_count=25) as requests_whaor:
#     pbar = enlighten.Counter(total=len(cashtags), desc="Exchange Search...", unit="symbols")
#     for chunk in chunked(cashtags, 1000):
#         with ThreadPoolExecutor(max_workers=25) as executor:
#             futures = [
#                 executor.submit(get, ct, proxies=requests_whaor.rotating_proxy) for ct in chunk
#             ]
#             for future in as_completed(futures):
#                 result = future.result()
#                 pbar.update()
#                 if result:
#                     print(result.json(indent=4))
#
#         requests_whaor.restart_onions()


# with NitterScraper(host="0.0.0.0", port=8008) as nitter:
#     for tweet in nitter.get_tweets(user, pages=100):
#         for cashtag in tweet.entries.cashtags:
#             result = fuzzy_symbol_seach(cashtag.replace("$", ""), first=True)
#             if result:
#                 print(result.json(indent=4))
#                 summary = get_summary_page(result.symbol, fuzzy_search=False)
#                 if summary:
#                     print(summary.json(indent=4))
