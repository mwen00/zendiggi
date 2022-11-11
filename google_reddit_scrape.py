"""
Query Google to get related Reddit posts
(FYI Reddit's internal search is v terrible)
TempDB: https://docs.google.com/spreadsheets/d/1-8i5Y7Tt6Vx1E9mzZ2hbIy8rI45Ng6DqTMQgPdg3tmw/edit#gid=0
"""

import urllib.request
from bs4 import BeautifulSoup
import re
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd


# TODO: Abstract this some more
class RedditPost:
    LEFT_URL_PATTERN = ".*comments/"

    def __init__(self, title, _url, location):
        self.location = location
        self.title = title
        self.identifier = self._parse_url(_url)

    def _parse_url(self, _url):
        # TODO: There has to be a more concise way to pattern match
        p = re.compile(self.LEFT_URL_PATTERN)
        # Retrieve all text right of the LEFT_URL_PATTERN
        right = p.sub("", _url)
        # Remove all the text right of the remaining "/"
        p = re.compile("/.*")
        return p.sub("", right)

    def __eq__(self, other):
        return self.identifier == other.identifier

    def __str__(self):
        return f"Location: {self.location}, Post Title: {self.title}, Post Identifier: {self.identifier}"


# PART 1: Google Query
# TODO: Allow for more results - e.g. can modify to page 2 with "&start=10"
def google_query(site, location, keywords=None):
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
def parse_html(html, location):
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

        try:
            # TODO: Probably better to not create the RedditPost to then discard a dup
            post = RedditPost(h3, url, location)
            if post not in results:
                results.append(post)
        except ValueError:
            print(f"Could not parse title and URL from {div}")

    return results


# TODO: Use an actual database once the db structure is determined
# PART 3: Connect to Google Sheets
def insert_posts(df):
    scope = ['https://www.googleapis.com/auth/spreadsheets',
             "https://www.googleapis.com/auth/drive"]

    credentials = ServiceAccountCredentials.from_json_keyfile_name("gs_credentials.json", scope)
    client = gspread.authorize(credentials)

    # Create new database
    # sheet = client.create("TempDatabase")

    # Share sheet with my Gmail accounts
    # sheet.share('melwen26@gmail.com', perm_type='user', role='writer')

    # Open database
    sheet = client.open("TempDatabase").sheet1

    # Export df to a sheet
    sheet.update([df.columns.values.tolist()] + df.values.tolist())


def main():
    # TODO: Remove hardcoding for testing
    # site = "Reddit.com"
    # location = "Los Angeles"
    # keywords = "recommendations"

    site = input("What site do you want to search? ")
    # TODO: add check against valid locations? Auto-complete with Google Maps API?
    location = input("Search location: ")
    keywords = input("Additional search keywords/phrase: ")

    google_html = google_query(site, location, keywords)
    query_results = parse_html(google_html, location)

    # TODO: Remove debugging
    # print(pd.DataFrame([vars(i) for i in query_results]))

    insert_posts(pd.DataFrame([vars(i) for i in query_results]))


if __name__ == "__main__":
    main()


