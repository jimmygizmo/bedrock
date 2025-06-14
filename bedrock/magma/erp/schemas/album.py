from pydantic import BaseModel, Field, field_validator
from typing import Optional
from magma.erp.schemas.shared import ArtistRead  # Replaced with ArtistSimpleRead to fix a nested lazy-loading loop.
from magma.erp.schemas.shared import ArtistSimpleRead
from magma.erp.schemas.shared import TrackSimpleRead
from magma.erp.schemas.track import TrackRead
from magma.validators.shared import validate_alnum_with_spaces


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
    @classmethod
    @field_validator('title')
    def v_title_alnum_with_spaces(cls, v: Optional[str]) -> Optional[str]:
        return validate_alnum_with_spaces(v, "Album.title")


# --------  READ (GET)  --------
class AlbumRead(ConfigBase):
    album_id: int = Field(..., alias="AlbumId")
    title: str = Field(..., alias="Title")
    artist: ArtistSimpleRead
    tracks: list[TrackSimpleRead]
    # TODO: TrackRead needs a custom tuned version for here. 1. Need not show Album of Track,
    # When this had ArtistRead, since that has albums, it created a nested, lazy-loading loop, which is another way
    #  you get greenlet errors.
    # TODO: UPDATE: Now has TrackSimpleRead, a quick shot at a cleaner view of Tracks via Album
    #   NAME IDEA for that cleaner read: TrckReadForAblumView

# --------  REFERENCE  --------
# NOTE: Bedrock does not use raw SQL for DB init. SQLAlchemy models are used. This SQL is only here for reference.
# CREATE TABLE album
# (
#     album_id INT NOT NULL GENERATED ALWAYS AS IDENTITY,
#     title VARCHAR(160) NOT NULL,
#     artist_id INT NOT NULL,
#     CONSTRAINT album_pkey PRIMARY KEY  (album_id)
# );

