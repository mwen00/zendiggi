from sqlalchemy import Column, Integer, String

from app.db.base_class import Base


class Location(Base):
    id = Column(Integer, primary_key=True, index=True)
    location = Column(String(256), nullable=False)
    source = Column(String(256), nullable=True)
    update_date = Column(String(256), nullable=False)
