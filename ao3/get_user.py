from .get_response import get_response


def get_user(user_name: str) -> dict[list]:
    """
    Get basic profile info (pseud, join date, user ID).

    :param user_name: AO3 username of interest.

    :return: profile as dict[list] in {column: row} format.
    """
    url = f"https://archiveofourown.org/users/{user_name}/profile/"
    soup = get_response(url)

    prof = soup.find("dl", {"class": "meta"}).find_all("dd")

    key = ["name", "date", "user_id"]
    value = [[p.text] for p in prof]

    return dict(zip(key, value))
