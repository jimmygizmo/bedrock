from pydantic import BaseModel, EmailStr, Field, field_validator, ConfigDict
from typing import Optional, List
from magma.erp.schemas.shared import ArtistRead


# ########    PYDANTIC SCHEMA:  album    ########


# -------- Base schema shared across input/output --------
class AlbumBase(BaseModel):
    album_id: int = Field(..., alias="AlbumId")
    title: str = Field(..., alias="Title")
    artist_id: int = Field(..., alias="ArtistId")

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
class AlbumRead(BaseModel):
    album_id: int
    title: str
    artist: ArtistRead

    class Config:
        from_attributes = True
        populate_by_name = True


# SQL CREATE from the original Chinook project for comparison with this Bedrock schema
#
# CREATE TABLE album
# (
#     album_id INT NOT NULL GENERATED ALWAYS AS IDENTITY,
#     title VARCHAR(160) NOT NULL,
#     artist_id INT NOT NULL,
#     CONSTRAINT album_pkey PRIMARY KEY  (album_id)
# );

