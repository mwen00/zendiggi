from pydantic import BaseModel


class RedditPostBase(BaseModel):
    id: str
    location: str
    rank: int
    title: str


class RedditPostCreate(RedditPostBase):
    id: str
    location: str
    rank: int
    title: str


class RedditPostUpdate(RedditPostBase):
    op_text: str
