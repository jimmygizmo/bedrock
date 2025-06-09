from pydantic import BaseModel, EmailStr, Field, field_validator, ConfigDict
from typing import Optional, List
from magma.schemas.artist import ArtistRead
from magma.schemas.track import TrackRead


# ########    PYDANTIC SCHEMA:  album    ########


# -------- Base schema shared across input/output --------
class AlbumBase(BaseModel):
    title: str
    artist_id: int

    class Config:
        from_attributes = True
        populate_by_name = True


# -------- Used for incoming POST data (POST: create a new album with new details) --------
class AlbumCreate(AlbumBase):

    # TODO: Enable this after ensuring our seed data is free of non-alpha charaters in this field.
    # @classmethod
    # @field_validator('title')
    # def title_alphanumeric(cls, v: Optional[str]) -> Optional[str]:
    #     if v is not None and not v.replace(" ", "").isalnum():
    #         raise ValueError("Field 'title' must be alphanumeric (spaces allowed)")
    #     return v

    # Many more validation methods will be going in a *Create class especially in other schemas with more fields.
    pass


# -------- Used for incoming POST data for *UPDATE* (PATCH/PUT: update album details for an existing album) --------
class AlbumUpdate(BaseModel):
    title: Optional[str] = None
    artist_id: Optional[int] = None

    class Config:
        from_attributes = True
        populate_by_name = True


# -------- Used for response serialization (GET: /albums/1) --------
class AlbumRead(BaseModel):  # "flat read" - no joins
    album_id: int
    title: str
    artist_id: int

    class Config:
        from_attributes = True
        populate_by_name = True


# -------- Used for response serialization (GET: /albums/1) --------
# EXAMPLE OF A JOIN SCHEMA
# Uses imported schemas: ArtistRead, TrackRead
# class AlbumDeepRead(BaseModel):  # "deep read" - includes relationships
#     album_id: int
#     title: str
#     artist_id: int
#     artist: Optional[ArtistRead] = None
#     tracks: Optional[List[TrackRead]] = []
#
#     class Config:
#         from_attributes = True
#         populate_by_name = True

