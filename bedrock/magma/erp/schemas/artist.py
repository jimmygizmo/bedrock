from pydantic import BaseModel, Field, field_validator
from typing import Optional, List
from magma.erp.schemas.shared import AlbumRead
from magma.validators.shared import validate_alnum_with_spaces


# ########    PYDANTIC SCHEMA:  artist    ########


# --------  CONFIG  --------
class ConfigBase(BaseModel):
    model_config = {
        "from_attributes": True,
        "populate_by_name": True,
    }


# --------  BASE  --------
class ArtistBase(ConfigBase):
    name: Optional[str] = Field(None, alias="Name", max_length=120)


# --------  CREATE (POST)  --------
class ArtistCreate(ArtistBase):
    # OPTION - We could enforce name being present in create by adding this override of ArtistBase in the following line:
    # name: str = Field(..., alias="Name", max_length=120)  # Disabled. Here as an example. NOTE: DB allows null here.
    @classmethod
    @field_validator('name')
    def v_name_alnum_with_spaces(cls, v: Optional[str]) -> Optional[str]:
        return validate_alnum_with_spaces(v, "Artist.name")


# --------  UPDATE (PUT)  --------
class ArtistUpdate(ConfigBase):
    name: Optional[str] = Field(None, alias="Name", max_length=120)
    @classmethod
    @field_validator('name')
    def v_name_alnum_with_spaces(cls, v: Optional[str]) -> Optional[str]:
        return validate_alnum_with_spaces(v, "Artist.name")


# --------  READ (GET)  --------
class ArtistRead(ConfigBase):
    artist_id: int = Field(..., alias="ArtistId")
    name: str = Field(..., alias="Name")
    # albums: List[AlbumRead] = []  # Making this optional below. No factors yet making [] a good default.
    albums: Optional[List[AlbumRead]] = None


# --------  REFERENCE  --------
# NOTE: Bedrock does not use raw SQL for DB init. SQLAlchemy models are used. This SQL is only here for reference.
# CREATE TABLE artist
# (
#     artist_id INT NOT NULL GENERATED ALWAYS AS IDENTITY,
#     name VARCHAR(120),
#     CONSTRAINT artist_pkey PRIMARY KEY  (artist_id)
# );

