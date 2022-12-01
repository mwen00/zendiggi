import praw
import os

from app.db.session import SessionLocal
from app import crud, schemas


def insert_reddit_comments(results) -> None:
    # Is this OK? opening up a session here and also when updating redditpost table?
    db = SessionLocal()

    # Reddit Credentials
    CLIENT_ID = os.getenv("CLIENT_ID")
    CLIENT_SECRET = os.getenv("CLIENT_SECRET")
    USER_AGENT = os.getenv("USER_AGENT")

    # Create Reddit instance
    reddit = praw.Reddit(client_id=CLIENT_ID,
                     client_secret=CLIENT_SECRET,
                     user_agent=USER_AGENT)

    for result in results:
        # Retrieve the post_id from each GoogleResult
        post_id = result.identifier

        # Obtain the Reddit submission obj
        submission = reddit.submission(post_id)

        # Update redditpost table to include the op text
        update_reddit_post_op(post_id,submission.selftext)

        # limit=0 removes all MoreComments obj from the CommentForest
        submission.comments.replace_more(limit=0)

        # Iterate through the CommentForest, a list of top-level comments
        for top_idx, top_level_comment in enumerate(submission.comments):
            # BFS of replies for the top_level_comment
            replies = ""

            # Concatenate all the subcomments into replies
            for comments in top_level_comment.replies.list():
                replies += " " + comments.body

            comment_in = schemas.RedditCommentCreate(
                post_id=post_id,
                rank=top_idx,
                top_comment=top_level_comment.body,
                replies=replies
            )

            crud.redditcomment.create(db, obj_in=comment_in)


def update_reddit_post_op(post_id: str, op_text: str) -> None:
    db = SessionLocal()

    post = crud.redditpost.get(db, id=post_id)

    # Not sure how to use the RedditPostUpdate Model here...
    post_in = {
        "op_text": op_text
    }
    
    crud.redditpost.update(db, db_obj=post, obj_in=post_in)
