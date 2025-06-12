from pydantic import BaseModel, Field, field_validator, ConfigDict
from typing import Optional, List
from magma.erp.schemas.shared import AlbumRead


# ########    PYDANTIC SCHEMA:  artist    ########


# -------- Configured BaseModel --------
class ConfigBase(BaseModel):
    class Config:
        from_attributes = True
        populate_by_name = True


# -------- Base schema shared across input/output --------
class ArtistBase(ConfigBase):
    name: Optional[str] = Field(..., alias="Name", max_length=120)


# -------- Used for incoming POST data (POST: create a new artist with new details) --------
class ArtistCreate(ArtistBase):
    # VALIDATOR - CREATE - name  # TODO: Refactor to shared validators.
    @classmethod
    @field_validator('name')
    def name_alphanumeric(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            v = v.strip()
            if not v.replace(" ", "").isalnum():
                raise ValueError("Field 'Artist.name' must be alphanumeric (spaces allowed)")
        return v


# -------- Used for incoming POST data for *UPDATE* (PATCH/PUT: update artist details for an existing artist) --------
class ArtistUpdate(ConfigBase):
    name: Optional[str] = Field(None, alias="Name", max_length=120)
    # VALIDATOR - UPDATE - name  # TODO: Refactor to shared validators.
    @classmethod
    @field_validator('name')
    def name_alphanumeric(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            v = v.strip()
            if not v.replace(" ", "").isalnum():
                raise ValueError("Field 'Artist.name' must be alphanumeric (spaces allowed)")
        return v


# -------- Used for response serialization (GET: /artists/1) --------
class ArtistRead(ConfigBase):
    artist_id: int = Field(..., alias="ArtistId")
    name: str = Field(..., alias="Name")
    albums: List[AlbumRead] = []


# SQL CREATE from the original Chinook project for comparison with this Bedrock schema
#
# CREATE TABLE artist
# (
#     artist_id INT NOT NULL GENERATED ALWAYS AS IDENTITY,
#     name VARCHAR(120),
#     CONSTRAINT artist_pkey PRIMARY KEY  (artist_id)
# );

