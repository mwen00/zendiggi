from pydantic import BaseModel


class LocationBase(BaseModel):
    location: str
    source: str
    update_date: str


class LocationCreate(LocationBase):
    location: str
    source: str
    update_date: str


class LocationUpdate(LocationBase):
    update_date: str
