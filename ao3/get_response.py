from random import randint
from time import sleep
from requests import get
from bs4 import BeautifulSoup


def get_response(url: str, pause: tuple[int, int] = (3, 6),
                 features: str = "html.parser") -> BeautifulSoup:
    """
    Perform a GET request on an AO3 page and return a bs4.BeautifulSoup
    instance for parsing. Waits a random number of seconds after the request
    to facilitate sequential calls.

    :param url: target URL.
    :param pause: (min, max) time in seconds between requests.
    :param features: `features` parameter utilized by bs4.BeautifulSoup call.

    :return: site content as a bs4.BeautifulSoup instance.

    """
    m, n = pause
    response = get(url)

    if response.status_code != 200:
        error_msg = f"GET request returned status code {response.status_code}"
    elif response.url == "https://archiveofourown.org/":
        error_msg = "GET request returned main page. URL doesn't exist."
    else:
        error_msg = None

    if error_msg is not None:
        raise ValueError(error_msg)
    else:
        sleep(randint(m, n))
        return BeautifulSoup(response.text, features=features)
