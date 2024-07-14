from datetime import datetime
from .get_response import get_response


def get_work(user_name: str) -> list[dict]:
    """
    Get top-level work metrics for a user's works on AO3.

    :param user_name: target user.

    :return: list[dict] where each dict is in {"column": "value"} row format.
    """
    url = f"https://archiveofourown.org/users/{user_name}/works?page=1"
    soup = get_response(url)

    navigation = soup.find("ol", {"role": "navigation"})
    if navigation is not None:
        end = int(navigation.text.split(" ")[-3])
    else:
        end = 1

    uid = None
    row = []
    for i in range(1, end + 1):
        if i != 1:
            url = url.replace(f"page={str(i - 1)}", f"page={str(i)}")
            soup = get_response(url)

        blurb = soup.find("ol", {"class": "work index group"})
        art = blurb.find_all("li", {"role": "article"})

        var = ["id", "date", "language", "words", "chapters", "comments",
               "kudos", "bookmarks", "hits"]
        int_var = ["words", "comments", "kudos", "bookmarks", "hits"]

        if i == 1:
            uid = list(filter(lambda s: s.find("user") >= 0, art[0]["class"]))
            uid = uid[0].replace("user-", "")

        for a in art:
            work = {"user_id": uid,
                    "id": a["id"].replace("work_", ""),
                    "title": a.find("h4").find("a").text,
                    "date": a.find("p", {"class": "datetime"}).text}

            stat = a.find("dl", {"class": "stats"})
            for key in var[2:]:
                value = stat.find("dd", {"class": key})
                if key in int_var:
                    if value is None:
                        work[key] = 0
                    else:
                        work[key] = int(value.text.replace(",", ""))
                else:
                    work[key] = "" if value is None else value.text

            work["date"] = datetime.strptime(work["date"], "%d %b %Y").date()

            row.append(work)

    return row
