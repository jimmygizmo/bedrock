from pydantic import BaseModel, Field


# ########    PYDANTIC SCHEMA:  playlist_track    ########


# --------  CONFIG  --------
class ConfigBase(BaseModel):
    model_config = {
        "from_attributes": True,
        "populate_by_name": True,
    }


# --------  BASE  --------
class PlaylistTrackBase(ConfigBase):
    playlist_id: int = Field(..., alias="PlaylistId")
    track_id: int = Field(..., alias="TrackId")


# --------  CREATE (POST)  --------
class PlaylistTrackCreate(PlaylistTrackBase):
    pass


# --------  UPDATE (PUT)  --------
class PlaylistTrackUpdate(PlaylistTrackBase):
    pass


# --------  READ (GET)  --------
class PlaylistTrackRead(ConfigBase):
    playlist_id: int = Field(..., alias="PlaylistId")
    track_id: int = Field(..., alias="TrackId")


# --------  REFERENCE  --------
# NOTE: Bedrock does not use raw SQL for DB init. SQLAlchemy models are used. This SQL is only here for reference.
# CREATE TABLE playlist_track
# (
#     playlist_id INT NOT NULL,
#     track_id INT NOT NULL,
#     CONSTRAINT playlist_track_pkey PRIMARY KEY  (playlist_id, track_id)
# );

