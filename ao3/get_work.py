from datetime import datetime
from .get_response import get_response


def get_work(user_name: str) -> list[dict]:
    """
    Get top-level work metrics for a user's works on AO3.

    :param user_name: target user.

    :return: list[dict] where each dict is in {"column": "value"} row format.
    """
    url = f"https://archiveofourown.org/users/{user_name}/works/"
    soup = get_response(url)

    # to do: paginate the process below.
    blurb = soup.find("ol", {"class": "work index group"})
    art = blurb.find_all("li", {"role": "article"})

    var = ["id", "date", "language", "words", "chapters", "comments",
           "kudos", "bookmarks", "hits"]
    int_var = ["words", "kudos", "bookmarks", "hits"]

    row = []
    for a in art:
        work = dict()

        work["id"] = a["id"].replace("work_", "")
        work["title"] = a.find("h4").find("a").text
        work["date"] = a.find("p", {"class": "datetime"}).text

        stat = a.find("dl", {"class": "stats"})
        for key in var[2:]:
            value = stat.find("dd", {"class": key})
            if key in int_var:
                work[key] = 0 if value is None else int(value.text)
            else:
                work[key] = "" if value is None else value.text

        work["date"] = datetime.strptime(work["date"], "%d %b %Y").date()

        row.append(work)

    return row
