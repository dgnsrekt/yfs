"""Send get requests."""

from typing import Dict

import requests
from requests import Response, Session


def requestor(
    url: str, session: Session = None, proxies: Dict[str, str] = None, timeout: int = 5
) -> Response:
    """Send get requests.

    Args:
        url (str): The url to send a request to.
        session (Session): A Session object to send a request with.
        proxies (dict): Dictionary mapping protocol to the URL of the proxy.
        timeout (int): How long to wait for the server to send a response.
    """
    # TODO: try and pass a session with retries plus whaor. pylint: disable=W0511
    if session:
        return session.get(url, proxies=proxies, timeout=timeout)

    return requests.get(url, proxies=proxies, timeout=timeout)
