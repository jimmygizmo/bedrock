from pydantic import BaseModel, Field
from typing import Optional
# from magma.schemas.genre import GenreRead
# from magma.schemas.media_type import MediaTypeRead
# from magma.schemas.invoice_line import InvoiceLineRead
# from magma.schemas.playlist_track import PlaylistTrackRead


# ########    PYDANTIC SCHEMA:  track    ########


# --------  CONFIG  --------
class ConfigBase(BaseModel):
    model_config = {
        "from_attributes": True,
        "populate_by_name": True,
    }


# --------  BASE  --------
class TrackBase(ConfigBase):
    name: str = Field(..., alias="Name")
    album_id: Optional[int] = Field(None, alias="AlbumId")
    media_type_id: int = Field(..., alias="MediaTypeId")
    genre_id: Optional[int] = Field(None, alias="GenreId")
    composer: Optional[str] = Field(None, alias="Composer")
    milliseconds: int = Field(..., alias="Milliseconds")
    bytes: Optional[int] = Field(None, alias="Bytes")
    unit_price: float = Field(..., alias="UnitPrice")


# --------  CREATE (POST)  --------
class TrackCreate(TrackBase):

    # TODO: Enable this after ensuring our seed data is free of empty/no-value in this field. AND update the code
    # Example validator placeholder
    # @classmethod
    # @field_validator('name')
    # def name_is_valid(cls, v: str) -> str:
    #     if not v or not v.strip():
    #         raise ValueError("Track name cannot be empty.")
    #     return v

    # TODO: Enable this after ensuring our seed data is free of non-alpha charaters in this field. AND update the code
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
class TrackUpdate(ConfigBase):
    name: Optional[str] = None
    album_id: Optional[int] = None
    media_type_id: Optional[int] = None
    genre_id: Optional[int] = None
    composer: Optional[str] = None
    milliseconds: Optional[int] = None
    bytes: Optional[int] = None
    unit_price: Optional[float] = None


# --------  READ (GET)  --------
class TrackRead(ConfigBase):
    track_id: int
    name: str
    album_id: Optional[int]
    media_type_id: int
    genre_id: Optional[int]
    composer: Optional[str]
    milliseconds: int
    bytes: Optional[int]
    unit_price: float


# EXAMPLE OF A JOIN SCHEMA
# Uses imported schemas: AlbumRead, MediaTypeRead, GenreRead, InvoiceLineRead, PlayListTrackRead
# class TrackDeepRead(ConfigBase):  # "deep read" - includes relationships
#     track_id: int
#     name: str
#     album_id: Optional[int]
#     media_type_id: int
#     genre_id: Optional[int]
#     composer: Optional[str]
#     milliseconds: int
#     bytes: Optional[int]
#     unit_price: float
#
#     album: Optional[AlbumRead] = None
#     media_type: Optional[MediaTypeRead] = None
#     genre: Optional[GenreRead] = None
#     invoice_lines: Optional[List[InvoiceLineRead]] = []
#     playlists: Optional[List[PlaylistTrackRead]] = []


# --------  REFERENCE  --------
# NOTE: Bedrock does not use raw SQL for DB init. SQLAlchemy models are used. This SQL is only here for reference.
# CREATE TABLE track
# (
#     track_id INT NOT NULL GENERATED ALWAYS AS IDENTITY,
#     name VARCHAR(200) NOT NULL,
#     album_id INT,
#     media_type_id INT NOT NULL,
#     genre_id INT,
#     composer VARCHAR(220),
#     milliseconds INT NOT NULL,
#     bytes INT,
#     unit_price NUMERIC(10,2) NOT NULL,
#     CONSTRAINT track_pkey PRIMARY KEY  (track_id)
# );

