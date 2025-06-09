from pydantic import BaseModel, Field, field_validator, ConfigDict
from typing import Optional, List
from magma.schemas.album import AlbumRead


# ########    PYDANTIC SCHEMA:  artist    ########


# -------- Base schema shared across input/output --------
class ArtistBase(BaseModel):
    name: Optional[str] = None

    class Config:
        from_attributes = True
        populate_by_name = True


# -------- Used for incoming POST data (POST: create a new artist with new details) --------
class ArtistCreate(ArtistBase):

    # TODO: Enable this after ensuring our seed data is free of non-alpha charaters in this field.
    # @classmethod
    # @field_validator('name')
    # def name_alphanumeric(cls, v: Optional[str]) -> Optional[str]:
    #     if v is not None and not v.replace(" ", "").isalnum():
    #         raise ValueError("Field 'name' must be alphanumeric (spaces allowed)")
    #     return v

    # Many more validation methods will be going in a *Create class especially in other schemas with more fields.
    pass


# -------- Used for incoming POST data for *UPDATE* (PATCH/PUT: update album details for an existing album) --------
class ArtistUpdate(BaseModel):
    name: Optional[str] = None

    class Config:
        from_attributes = True
        populate_by_name = True


# -------- Used for response serialization (GET: /artists/1) --------
class ArtistRead(BaseModel):  # "flat read" - no joins
    artist_id: int
    name: Optional[str] = None

    class Config:
        from_attributes = True
        populate_by_name = True


# -------- Used for response serialization (GET: /artists/1) --------
# EXAMPLE OF A JOIN SCHEMA
# Uses imported schema: AlbumRead which lives in schemas/album.py
# class ArtistDeepRead(BaseModel):  # "deep read" - includes relationships
#     artist_id: int
#     name: Optional[str] = None
#     albums: Optional[List[AlbumRead]] = []
#
#     class Config:
#         from_attributes = True
#         populate_by_name = True

