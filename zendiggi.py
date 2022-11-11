import os
from dotenv import load_dotenv
import praw
from pprint import pprint


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
# submission = reddit.submission("39zje0")
# print(submission.title)  # to make it non-lazy
# pprint(vars(submission))

# Working with Streams
# for comment in reddit.subreddit("test").stream.comments():
#     print(comment)

# for submission in reddit.subreddit("all").stream.submissions():
#     print(submission)

url = "https://www.reddit.com/r/LosAngeles/comments/be5rj/visiting_la_for_8_days_i_have_tons_of_questions/"
submission = reddit.submission(url=url)
# Or can use: submission = reddit.submission("be5rj")

for top_level_comment in submission.comments:
    print(top_level_comment.body)

