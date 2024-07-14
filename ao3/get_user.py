from datetime import date
from .get_response import get_response


def get_user(user_name: str) -> dict[str]:
    """
    Get basic profile info for an AO3 user.

    :param user_name: AO3 username of interest.

    :return: table row in dict[str] format such that {"column": "value"}.
    """
    url = f"https://archiveofourown.org/users/{user_name}/profile/"
    soup = get_response(url)

    prof = soup.find("dl", {"class": "meta"}).find_all("dd")

    key = ["name", "date", "id"]
    value = [p.text for p in prof]

    row = dict(zip(key, value))
    row["date"] = date.fromisoformat(row["date"])

    return row
