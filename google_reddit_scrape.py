"""
Query Google to get related Reddit posts
(FYI Reddit's internal search is v terrible)
TempDB: https://docs.google.com/spreadsheets/d/1-8i5Y7Tt6Vx1E9mzZ2hbIy8rI45Ng6DqTMQgPdg3tmw/edit#gid=0
"""
import os
from dotenv import load_dotenv
from datetime import date
from typing import List
from typing import TypeVar

import firebase_admin
from firebase_admin import firestore

import urllib.request
from bs4 import BeautifulSoup
import re


load_dotenv()
T = TypeVar('T')

# Initialize connection to Firestore db
cred = firebase_admin.credentials.Certificate("google_credentials.json")
app = firebase_admin.initialize_app(cred)
db = firestore.client()


# TODO: Abstract this out some more
class RedditPost:
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


# PART 1: Google Query
# TODO: Allow for more results - e.g. can modify to page 2 with "&start=10"
def google_query(site: str, location: str, keywords: str = None) -> str:
    base_url = "https://www.google.com/search?q=site%3A"
    s = location + " " + keywords
    query = base_url + site + '+' + '+'.join(s.split())

    # Mask automation by adding User Agent to the request header
    user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) " \
                 "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"

    req = urllib.request.Request(query)
    req.add_header('User-Agent', user_agent)

    # Read response into var
    with urllib.request.urlopen(req) as response:
        html = response.read()

    return html


# PART 2: Parse Google HTML
def parse_html(html: str, location: str) -> List[RedditPost]:
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
        # PEP 572: OK use of walrus operator?
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
            post = RedditPost(h3, url, location)
            if post not in results:
                results.append(post)
        except ValueError:
            print(f"Could not parse title and URL from {div}")

    return results


# PART 3: Insert Reddit posts into db
def insert_reddit_posts(posts: List[RedditPost]):
    db.collection("locations").document(posts[0].location).set({
        "update_date": date.today().isoformat(),
        "posts": [post.identifier for post in posts]
    }, merge=True)


# Check if the location is in the db or over a year since last update
def verify_loc_exists(location: str) -> bool:
    doc_ref = db.collection("locations").document(location)
    doc = doc_ref.get()

    return True if doc.exists else False


# Retrieve posts if the location exists in the db and last update was within a year
def get_posts(location: str):
    data = db.collection("locations").document(location).get().to_dict()
    last_update = date.fromisoformat(data["update_date"])

    # TODO: Implement re-scrape if data is old and append to results, need some sort of global state for the user query
    if (date.today() - last_update).days > 10:
        pass

    print(f"Data for location {location} already exists from {last_update}.")


def main():
    # TODO: Remove hardcoding for testng
    site = "Reddit.com"
    location = "Yakushima"
    keywords = "recommendations"

    # site = input("What site do you want to search? ")
    # # TODO: add check against valid locations? Auto-complete with Google Maps API?
    # location = input("Search location: ")
    # keywords = input("Additional search keywords/phrase: ")

    # Check if the location is already in the db
    if verify_loc_exists(location):
        get_posts(location)
    else:
        # Add new location and post to the db
        google_html = google_query(site, location, keywords)
        query_results = parse_html(google_html, location)
        insert_reddit_posts(query_results)


if __name__ == "__main__":
    main()
