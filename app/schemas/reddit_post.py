from pydantic import BaseModel


class RedditPostBase(BaseModel):
    location: str
    rank: int
    title: str
    op_text: str


class RedditPostCreate(RedditPostBase):
    location: str
    rank: int
    title: str
    op_text: str


class RedditPostUpdate(RedditPostBase):
    location: str
    rank: int
    title: str
    op_text: str