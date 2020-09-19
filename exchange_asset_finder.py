from nitter_scraper import NitterScraper
from yfs.symbol import fuzzy_symbol_seach
from yfs.summary import get_summary_page, get_summary_pages

user = "eWhispers"

with NitterScraper(host="0.0.0.0", port=8008) as nitter:
    for tweet in nitter.get_tweets(user, pages=100):
        cashtags = [cashtag.replace("$", "") for cashtag in tweet.entries.cashtags]
        results = get_summary_pages(cashtags, with_threads=True)
        if results:
            print(results.dataframe)


# with NitterScraper(host="0.0.0.0", port=8008) as nitter:
#     for tweet in nitter.get_tweets(user, pages=100):
#         for cashtag in tweet.entries.cashtags:
#             result = fuzzy_symbol_seach(cashtag.replace("$", ""), first=True)
#             if result:
#                 print(result.json(indent=4))
#                 summary = get_summary_page(result.symbol, fuzzy_search=False)
#                 if summary:
#                     print(summary.json(indent=4))
