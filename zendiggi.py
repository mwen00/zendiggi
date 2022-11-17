import pandas as pd
import praw
from pprint import pprint
from google_reddit_scrape import *


# Retrieve Reddit Credentials
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
USER_AGENT = os.getenv("USER_AGENT")

# Create Reddit instance
reddit = praw.Reddit(client_id=CLIENT_ID,
                     client_secret=CLIENT_SECRET,
                     user_agent=USER_AGENT)

# List of test comments
submissions = ["be5rj", "vmch7l", "r9bqwt"]
data = []

# Iterate through each submission/post
for i in submissions:
    # Obtain the Reddit submission obj
    submission = reddit.submission(i)

    # limit=0 removes all MoreComments obj from the CommentForest
    submission.comments.replace_more(limit=0)
    # Iterate through the CommentForest, a list of top-level comments
    for top_level_comment in submission.comments:
        # BFS of replies for the top_level_comment
        replies = ""

        for comments in top_level_comment.replies.list():
            replies += " " + comments.body

        post_details = {
            "identifier": i,
            "subreddit": submission.subreddit_name_prefixed,
            "title": submission.title,
            "selftext": submission.selftext,
            "top_level_comment": top_level_comment.body,
            "replies": replies
        }

        data.append(post_details)

df = pd.DataFrame(data, columns=['identifier', 'subreddit', 'title', 'selftext', 'top_level_comment', 'replies'])


def insert_comments(df):
    scope = ['https://www.googleapis.com/auth/spreadsheets',
             "https://www.googleapis.com/auth/drive"]

    credentials = ServiceAccountCredentials.from_json_keyfile_name("google_credentials.json", scope)
    client = gspread.authorize(credentials)

    # This is sheet2
    sheet = client.open("TempDatabase").get_worksheet(1)

    sheet.update([df.columns.values.tolist()] + df.values.tolist())


insert_comments(df)
