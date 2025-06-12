from pydantic import BaseModel, Field, field_validator, ConfigDict
from typing import Optional, List, TYPE_CHECKING
# from magma.erp.schemas.genre import GenreRead
# from magma.erp.schemas.media_type import MediaTypeRead
# from magma.erp.schemas.invoice_line import InvoiceLineRead
# from magma.erp.schemas.playlist_track import PlaylistTrackRead


# ########    PYDANTIC SCHEMA:  track    ########


# --------  CONFIG  --------
class ConfigBase(BaseModel):
    class Config:
        from_attributes = True
        populate_by_name = True


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
    # TODO: /magma/validators/shared.py has two validator examples there intended to use HERE. Complete and implement.
    pass


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


# --------  READ (GET)  -  (Early, in-progress developing relation views.)  FLAT, NO JOINS  --------
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


# IN-PROGRESS WORK:
# FIX ATTEMPT FOR CIRCULAR IMPORT - RETAINED FOR NOW - DOES ALSO SHOW INHERITANCE FROM TrackBase
# -------- Used for response serialization (GET: /tracks/1) --------
# class TrackRead(TrackBase):  # "flat read" - no joins
#     track_id: int
#
#     album: Optional["AlbumRead"] = None  # Forward reference as a string
#
#     # class Config:
#     #     from_attributes = True
#     #     populate_by_name = True
#
#
# # Do NOT import AlbumRead at the top!
# from magma.schemas.album import AlbumRead
# TrackRead.model_rebuild()


# IN-PROGRESS WORK:
# EXAMPLE OF A JOIN SCHEMA - EARLY, no notes seen on how this one worked so we can try it and/or delete this example.
# Uses imported schemas: AlbumRead, MediaTypeRead, GenreRead, InvoiceLineRead, PlayListTrackRead
# class TrackDeepRead(BaseModel):  # "deep read" - includes relationships
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
#
#     class Config:
#         from_attributes = True
#         populate_by_name = True


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

