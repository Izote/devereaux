from requests import get
from bs4 import BeautifulSoup


def get_user(user_name: str) -> list[str]:
    """
    Get basic profile info (pseud, join date, user ID).

    :param user_name: AO3 username of interest.
    :return: profile information as a list[str], ['pseud', 'yyy-mm-dd', 'id'].
    """
    url = f"https://archiveofourown.org/users/{user_name}/profile/"
    response = get(url)

    if response.status_code != 200:
        msg = (f"user '{user_name}' may not exist: "
               f"HTML Error code {response.status_code} returned.")

        raise ValueError(msg)
    elif response.url == "https://archiveofourown.org/":
        raise ValueError(f"user '{user_name}' does not exist.")
    else:
        soup = BeautifulSoup(response.text, features="html.parser")

        profile = soup.find("dl", {"class": "meta"}).find_all("dd")
        profile = [p.text for p in profile]

        return profile
