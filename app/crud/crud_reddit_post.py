from app.crud.base import CRUDBase
from app.models.reddit_post import RedditPost
from app.schemas.reddit_post import RedditPostCreate, RedditPostUpdate


class CRUDRedditPost(CRUDBase[RedditPost, RedditPostCreate, RedditPostUpdate]):
    ...


redditpost = CRUDRedditPost(RedditPost)
