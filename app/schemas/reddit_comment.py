from pydantic import BaseModel


class RedditCommentBase(BaseModel):
    rank: int
    top_comment: str
    replies: str


class RedditCommentCreate(RedditCommentBase):
    rank: int
    post_id: str
    top_comment: str
    replies: str


class RedditCommentUpdate(RedditCommentBase):
    top_comment: str
    replies: str
