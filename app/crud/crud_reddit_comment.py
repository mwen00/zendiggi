from app.crud.base import CRUDBase
from app.models.reddit_comment import RedditComment
from app.schemas.reddit_comment import RedditCommentCreate, RedditCommentUpdate


class CRUDRedditComment(CRUDBase[RedditComment, RedditCommentCreate, RedditCommentUpdate]):
    ...


redditcomment = CRUDRedditComment(RedditComment)
