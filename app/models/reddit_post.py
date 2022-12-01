from sqlalchemy import Column, Integer, String
# from sqlalchemy.orm import relationship

from app.db.base_class import Base

# TODO: Maybe add in additional search params & probably a better way to link with location table
class RedditPost(Base):
    id = Column(String(256), primary_key=True, index=True)
    location = Column(String(256), nullable=False)
    rank = Column(Integer, nullable=False)
    title = Column(String(256), nullable=True)
    op_text = Column(String(1000), nullable=True)
    # comments = relationship("RedditComment", backref="redditpost")
