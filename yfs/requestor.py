import requests


def requestor(url, session=None, proxies=None, timeout=5):

    if session:
        return session.get(url, proxies=proxies, timeout=timeout)
    else:
        return requests.get(url, proxies=proxies, timeout=timeout)
