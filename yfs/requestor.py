from typing import Dict

import requests
from requests import Session


def requestor(url, session: Session = None, proxies: Dict = None, timeout: int = 5):

    # response ok should be here. This will allow recursive reties.
    # maybe use an env var to set the retry limit
    # default retry 0

    if session:
        return session.get(url, proxies=proxies, timeout=timeout)
    else:
        return requests.get(url, proxies=proxies, timeout=timeout)
