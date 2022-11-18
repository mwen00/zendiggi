import praw
from google_reddit_scrape import *


# Reddit Credentials
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
USER_AGENT = os.getenv("USER_AGENT")

# Create Reddit instance
reddit = praw.Reddit(client_id=CLIENT_ID,
                     client_secret=CLIENT_SECRET,
                     user_agent=USER_AGENT)

# DB paths and document fields
REDDIT_POSTS_COLLECTION = "reddit_posts"
COMMENTS_COLLECTION = "comments"
POSTS_FIELD = "posts"


# TODO: Fix logic for when this occurs
# Read Reddit post ids from db
def get_ids(location: str) -> List[str]:
    try:
        data = db.collection(LOCATIONS_COLLECTION).document(location).get().to_dict()
        # Google search ranking is preserved with the post id order
        return data[POSTS_FIELD]
    except TypeError:
        print(f"Could not fetch Reddit post ids for {location}")


# Write post data to db
# TODO: Add check to speed up the process if the data exists
def insert_data(post_ids: List[str]):
    for idx, i in enumerate(post_ids):
        # Obtain the Reddit submission obj
        post = reddit.submission(i)

        # limit=0 removes all MoreComments obj from the CommentForest
        post.comments.replace_more(limit=0)
        # Iterate through the CommentForest, a list of top-level comments
        for top_idx, top_level_comment in enumerate(post.comments):
            # BFS of replies for the top_level_comment
            replies = ""

            for comments in top_level_comment.replies.list():
                replies += " " + comments.body

            # Add the post_id as a document
            db.collection(REDDIT_POSTS_COLLECTION).document(i).set({
                "google_search_rank": idx,
                "subreddit": post.subreddit_name_prefixed,
                "title": post.title,
                "selftext": post.selftext
            }, merge=True)

            # Add a sub-collection to the newly created post_id document with the comments
            db.collection(REDDIT_POSTS_COLLECTION).document(i).collection(COMMENTS_COLLECTION).add({
                "comment_rank": top_idx,
                "top_level_comment": top_level_comment.body,
                "replies": replies
            })


def main():
    location = input("Enter a location that already exists in the db: ")
    post_ids = get_ids(location)

    if post_ids:
        insert_data(post_ids)


if __name__ == "__main__":
    main()