from pydantic import BaseModel
from typing import List


class AlbumRead(BaseModel):
    id: int
    title: str

    class Config:
        from_attributes = True
        populate_by_name = True


class ArtistRead(BaseModel):
    id: int
    name: str
    albums: List[AlbumRead] = []

    class Config:
        from_attributes = True
        populate_by_name = True

