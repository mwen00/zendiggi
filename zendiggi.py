import os

import pandas as pd
from dotenv import load_dotenv
import praw
from pprint import pprint
from google_reddit_scrape import *


# Create Reddit instance
# Retrieve credentials
load_dotenv()
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
USER_AGENT = os.getenv("USER_AGENT")

reddit = praw.Reddit(client_id=CLIENT_ID,
                     client_secret=CLIENT_SECRET,
                     user_agent=USER_AGENT)

# Example: hot posts from r/all
# for submission in reddit.subreddit("all").hot(limit=25):
#     print(submission.title)

# Example: Determine Available Attributes of a PRAW Object
submission = reddit.submission("39zje0")
# print(submission)
print(submission.title)  # to make it non-lazy
# pprint(vars(submission))

# Working with Streams
# for comment in reddit.subreddit("test").stream.comments():
#     print(comment)

# for submission in reddit.subreddit("all").stream.submissions():
#     print(submission)

# List of test comments
submissions = ["be5rj", "vmch7l", "r9bqwt", "suu23h", "pojpp5", "cr0z9", "wrr1uc", "sq4p9j", "suebs2", "sgni78"]

# Parsing examples:
# url = "https://www.reddit.com/r/LosAngeles/comments/be5rj/visiting_la_for_8_days_i_have_tons_of_questions/"
# submission = reddit.submission(url=url)
# Or can use: submission = reddit.submission("be5rj")

# TODO: create matrix of Top Level comment and concatenated sub comments
# top_comments = []
#
# for i in range(len(submissions)):
#     s = reddit.submission(submissions[i])
#     print(s)
    # for comment in reddit.submission(submissions[0]).comments:
    #     top_comments.append(comment)

# df = pd.DataFrame(top_comments, columns=['Top'])
#
# print(df)

# print(reddit.submission("be5rj"))

def insert_comments(df):
    pass
