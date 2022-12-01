from sqlalchemy import Column, Integer, String, ForeignKey

from app.db.base_class import Base


class RedditComment(Base):
    id = Column(Integer, primary_key=True, index=True)
    # TODO: Foreign Key relationship is NOT working
    # post_id = Column(String(256), ForeignKey("redditpost.id"))
    post_id = Column(String(256), nullable=False)
    rank = Column(Integer, nullable=False)
    top_comment = Column(String(1000), nullable=False)
    replies = Column(String(1000), nullable=True)
