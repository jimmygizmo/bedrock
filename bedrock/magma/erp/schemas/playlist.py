from pydantic import BaseModel, Field, field_validator
from typing import Optional
from magma.validators.shared import validate_alnum_with_spaces


# ########    PYDANTIC SCHEMA:  playlist    ########


# --------  CONFIG  --------
class ConfigBase(BaseModel):
    model_config = {
        "from_attributes": True,
        "populate_by_name": True,
    }


# --------  BASE  --------
class PlaylistBase(ConfigBase):
    name: Optional[str] = Field(None, alias="Name", max_length=120)


# --------  CREATE (POST)  --------
class PlaylistCreate(PlaylistBase):
    name: str = Field(..., alias="Name", max_length=120)

    @classmethod
    @field_validator("name")
    def v_name_alnum_with_spaces(cls, v: Optional[str], field) -> Optional[str]:
        return validate_alnum_with_spaces(v, f"Playlist.{field.name}")


# --------  UPDATE (PUT)  --------
class PlaylistUpdate(PlaylistBase):
    @classmethod
    @field_validator("name")
    def v_name_alnum_with_spaces(cls, v: Optional[str], field) -> Optional[str]:
        return validate_alnum_with_spaces(v, f"Playlist.{field.name}")


# --------  READ (GET)  --------
class PlaylistRead(ConfigBase):
    playlist_id: int = Field(..., alias="PlaylistId")
    name: Optional[str] = Field(None, alias="Name")


# --------  REFERENCE  --------
# NOTE: Bedrock does not use raw SQL for DB init. SQLAlchemy models are used. This SQL is only here for reference.
# CREATE TABLE playlist
# (
#     playlist_id INT NOT NULL GENERATED ALWAYS AS IDENTITY,
#     name VARCHAR(120),
#     CONSTRAINT playlist_pkey PRIMARY KEY  (playlist_id)
# );

