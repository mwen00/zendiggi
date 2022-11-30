from sqlalchemy import Column, Integer, String, ForeignKey

from app.db.base_class import Base


class RedditComment(Base):
    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(String(256), ForeignKey("redditpost.id"))
    rank = Column(Integer, nullable=False)
    top_comment = Column(String(1000), nullable=False)
    comment_tree = Column(String(1000), nullable=True)
