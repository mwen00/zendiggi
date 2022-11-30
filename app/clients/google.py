import logging

from bs4 import BeautifulSoup
import urllib.request
import re

from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app import crud, schemas

from datetime import date
from typing import List
from typing import TypeVar

# TO_REMOVE: 
logging.basicConfig(level=logging.DEBUG)


T = TypeVar('T')
GOOGLE_BASE_URL = "https://www.google.com/search?q=site%3A"
TARGET_WEBSITE = "Reddit.com"
USER_AGENT_DATA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) " \
                 "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"


# TODO: This is all very specific to retrieving data from Reddit
class GoogleResult:
    LEFT_URL_PATTERN = ".*comments/"

    def __init__(self, title: str, _url: str, location: str):
        self.location = location
        self.title = title
        # post init method when using dataclass
        self.identifier = self._parse_url(_url)

    def _parse_url(self, _url: str) -> str:
        # TODO: There has to be a more concise way to pattern match
        p = re.compile(self.LEFT_URL_PATTERN)
        # Retrieve all text right of the LEFT_URL_PATTERN
        right = p.sub("", _url)
        # Remove all the text right of the remaining "/"
        p = re.compile("/.*")
        return p.sub("", right)

    def __eq__(self, other: T) -> bool:
        return self.identifier == other.identifier

    def __str__(self) -> str:
        return f"Location: {self.location}, Post Title: {self.title}, Post Identifier: {self.identifier}"


def query_google(location: str, keywords: str = "recommendations") -> None:
    base_url = GOOGLE_BASE_URL
    s = location + " " + keywords
    query = base_url + TARGET_WEBSITE + '+' + '+'.join(s.split())

    # Mask automation by adding User Agent to the request header
    user_agent = USER_AGENT_DATA

    req = urllib.request.Request(query)
    req.add_header('User-Agent', user_agent)

    # Read response into var
    with urllib.request.urlopen(req) as response:
        html = response.read()

    parse_google_html(location, html)


def parse_google_html(location: str, html: str) -> List[GoogleResult]:
    # Construct the soup object to parse
    soup = BeautifulSoup(html, "html.parser")

    # TODO: Update to not target on div "MjjYud", soup.find_all('a') and then filter
    # Find all the search result divs
    results = []

    divs = soup.select("#search div.MjjYud")
    for div in divs:
        h3 = ""
        url = ""
        # Target nested divs that are returned in list
        if result_name := div.select("h3"):
            h3 = result_name[0].get_text()

        if result_url := div.select("a"):
            url = result_url[0].get("href")

        # Add a guard against non-comments
        if "comment" not in url:
            continue

        try:
            # TODO: Probably better to not create the RedditPost to then discard a dup
            # Maybe a set is more performant?
            post = GoogleResult(h3, url, location)
            if post not in results:
                results.append(post)
        except ValueError:
            logging.warn(f"Could not parse title and URL from {div}")

    # TODO: Move this...should I be opening two different sessions to write to two different tables?
    # insert_location(location)
    # insert_reddit_posts(location, results)

    logging.debug(results)

    # TO_REMOVE:
    write_log(results)


def insert_location(location: str) -> None:
    db = SessionLocal()

    # NOTE: There's an issue with SQLAlchemy typechecking for Date type. Sqlite can't handle date and datetime anyways
    current_date = str(date.today())

    location_in = schemas.LocationCreate(
        location=location,
        source=TARGET_WEBSITE,
        update_date=current_date
    )

    crud.location.create(db, obj_in=location_in)


def insert_reddit_posts(location: str, results: List[GoogleResult]) -> None:
    db = SessionLocal()
    
    for idx, result in enumerate(results):
        with open("log.txt", mode="a") as log:
            log.write(f"index: {idx}, {str(result)}" + "\n")

        post_in = schemas.RedditPostCreate(
            id=result.identifier,
            location=location, # How do I get the location.id as this value and define the foreign key properly?
            rank=idx,
            title=result.title
        )

        crud.redditpost.create(db, obj_in=post_in)


# TO_REMOVE:
def write_log(results: List[GoogleResult]) -> None:
    with open("log.txt", mode="a") as log:
        for i in results:
            log.write(str(i) + "\n")


# def main() -> None:
#     ...


# if __name__ == "__main__":
#     main()
