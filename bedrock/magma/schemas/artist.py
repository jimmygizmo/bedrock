from pydantic import BaseModel, Field
from typing import Optional, List
from magma.schemas.shared import AlbumRead


# ########    PYDANTIC SCHEMA:  artist    ########


# --------  CONFIG  --------
class ConfigBase(BaseModel):
    model_config = {
        "from_attributes": True,
        "populate_by_name": True,
    }


# --------  BASE  --------
class ArtistBase(ConfigBase):
    name: Optional[str] = Field(None, alias="Name")


# --------  CREATE (POST)  --------
class ArtistCreate(ArtistBase):

    # TODO: Enable this after ensuring our seed data is free of non-alpha charaters in this field.
    # @classmethod
    # @field_validator('name')
    # def name_alphanumeric(cls, v: Optional[str]) -> Optional[str]:
    #     if v is not None and not v.replace(" ", "").isalnum():
    #         raise ValueError("Field 'name' must be alphanumeric (spaces allowed)")
    #     return v

    # Many more validation methods will be going in a *Create class especially in other schemas with more fields.

    model_config = {
        "extra": "forbid",
    }


# --------  UPDATE (PUT)  --------
class ArtistUpdate(ConfigBase):
    name: Optional[str] = None


# --------  READ (GET)  --------
class ArtistRead(ConfigBase):
    artist_id: int
    name: str
    albums: List[AlbumRead] = []



# --------  REFERENCE  --------
# NOTE: Bedrock does not use raw SQL for DB init. SQLAlchemy models are used. This SQL is only here for reference.
# CREATE TABLE artist
# (
#     artist_id INT NOT NULL GENERATED ALWAYS AS IDENTITY,
#     name VARCHAR(120),
#     CONSTRAINT artist_pkey PRIMARY KEY  (artist_id)
# );

