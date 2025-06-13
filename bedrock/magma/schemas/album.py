from pydantic import BaseModel, Field, field_validator
from typing import Optional
from magma.schemas.shared import ArtistRead


# ########    PYDANTIC SCHEMA:  album    ########


# --------  CONFIG  --------
class ConfigBase(BaseModel):
    model_config = {
        "from_attributes": True,
        "populate_by_name": True,
    }


# --------  BASE  --------
class AlbumBase(ConfigBase):
    album_id: int = Field(..., alias="AlbumId")
    title: str = Field(..., alias="Title")
    artist_id: int = Field(..., alias="ArtistId")


# --------  CREATE (POST)  --------
class AlbumCreate(AlbumBase):
    @classmethod
    @field_validator('title')
    def v_title_alnum_with_spaces(cls, v: Optional[str]) -> Optional[str]:
        return validate_alnum_with_spaces(v, "Album.title")


# --------  UPDATE (PUT)  --------
class AlbumUpdate(ConfigBase):
    title: Optional[str] = None
    artist_id: Optional[int] = None


# --------  READ (GET)  --------
class AlbumRead(ConfigBase):
    album_id: int
    title: str
    artist: ArtistRead


# --------  REFERENCE  --------
# NOTE: Bedrock does not use raw SQL for DB init. SQLAlchemy models are used. This SQL is only here for reference.
# CREATE TABLE album
# (
#     album_id INT NOT NULL GENERATED ALWAYS AS IDENTITY,
#     title VARCHAR(160) NOT NULL,
#     artist_id INT NOT NULL,
#     CONSTRAINT album_pkey PRIMARY KEY  (album_id)
# );

