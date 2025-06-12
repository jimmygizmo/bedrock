from pydantic import BaseModel, Field, field_validator, ConfigDict
from typing import Optional, List
from magma.erp.schemas.shared import AlbumRead
from magma.validators.shared import validate_alnum_with_spaces


# ########    PYDANTIC SCHEMA:  artist    ########


# -------- Configured BaseModel --------
class ConfigBase(BaseModel):
    class Config:
        from_attributes = True
        populate_by_name = True


# -------- Base schema shared across input/output --------
class ArtistBase(ConfigBase):
    name: Optional[str] = Field(None, alias="Name", max_length=120)


# -------- Used for incoming POST data (POST: create a new artist with new details) --------
class ArtistCreate(ArtistBase):
    # OPTION - We could enforce name being present in create by adding this override of ArtistBase in the following line:
    # name: str = Field(..., alias="Name", max_length=120)  # Disabled. Here as an example. NOTE: DB allows null here.
    @classmethod
    @field_validator('name')
    def v_name_alnum_with_spaces(cls, v: Optional[str]) -> Optional[str]:
        return validate_alnum_with_spaces(v, "Artist.name")
    # def name_alphanumeric(cls, v: Optional[str]) -> Optional[str]:
    #     if v is not None:
    #         v = v.strip()
    #         if not v.replace(" ", "").isalnum():
    #             raise ValueError("Field 'Artist.name' must be alphanumeric (spaces allowed)")
    #     return v


# -------- Used for incoming POST data for *UPDATE* (PATCH/PUT: update artist details for an existing artist) --------
class ArtistUpdate(ConfigBase):
    name: Optional[str] = Field(None, alias="Name", max_length=120)
    @classmethod
    @field_validator('name')
    def v_name_alnum_with_spaces(cls, v: Optional[str]) -> Optional[str]:
        return validate_alnum_with_spaces(v, "Artist.name")
    # def name_alphanumeric(cls, v: Optional[str]) -> Optional[str]:
    #     if v is not None:
    #         v = v.strip()
    #         if not v.replace(" ", "").isalnum():
    #             raise ValueError("Field 'Artist.name' must be alphanumeric (spaces allowed)")
    #     return v


# -------- Used for response serialization (GET: /artists/1) --------
class ArtistRead(ConfigBase):
    artist_id: int = Field(..., alias="ArtistId")
    name: str = Field(..., alias="Name")
    # albums: List[AlbumRead] = []  # Making this optional below. No factors yet making [] a good default.
    albums: Optional[List[AlbumRead]] = None


# SQL CREATE from the original Chinook project for comparison with this Bedrock schema
#
# CREATE TABLE artist
# (
#     artist_id INT NOT NULL GENERATED ALWAYS AS IDENTITY,
#     name VARCHAR(120),
#     CONSTRAINT artist_pkey PRIMARY KEY  (artist_id)
# );

