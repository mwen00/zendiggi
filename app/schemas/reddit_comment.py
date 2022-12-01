from pydantic import BaseModel


class RedditCommentBase(BaseModel):
    rank: int
    top_comment: str
    replies: str


class RedditCommentCreate(RedditCommentBase):
    post_id: str
    rank: int
    top_comment: str
    replies: str


class RedditCommentUpdate(RedditCommentBase):
    top_comment: str
    replies: str
