from pydantic import BaseModel, Field, field_validator, ConfigDict
from typing import Optional, List
from magma.schemas.album import AlbumRead
# from magma.schemas.genre import GenreRead
# from magma.schemas.media_type import MediaTypeRead
# from magma.schemas.invoice_line import InvoiceLineRead
# from magma.schemas.playlist_track import PlaylistTrackRead


# ########    PYDANTIC SCHEMA:  track    ########


# -------- Base schema shared across input/output --------
class TrackBase(BaseModel):
    name: str
    album_id: Optional[int] = None
    media_type_id: int
    genre_id: Optional[int] = None
    composer: Optional[str] = None
    milliseconds: int
    bytes: Optional[int] = None
    unit_price: float

    class Config:
        from_attributes = True
        populate_by_name = True


# -------- Used for incoming POST data (POST: create a new track with new details) --------
class TrackCreate(TrackBase):

    # Example validator placeholder
    # @classmethod
    # @field_validator('name')
    # def name_is_valid(cls, v: str) -> str:
    #     if not v or not v.strip():
    #         raise ValueError("Track name cannot be empty.")
    #     return v

    # TODO: Enable this after ensuring our seed data is free of non-alpha charaters in this field.
    # @classmethod
    # @field_validator('name')
    # def name_alphanumeric(cls, v: Optional[str]) -> Optional[str]:
    #     if v is not None and not v.replace(" ", "").isalnum():
    #         raise ValueError("Field 'name' must be alphanumeric (spaces allowed)")
    #     return v

    # Many more validation methods will be going in a *Create class especially in other schemas with more fields.
    pass


# -------- Used for incoming POST data for *UPDATE* (PATCH/PUT: update track details for an existing track) --------
class TrackUpdate(BaseModel):
    name: Optional[str] = None
    album_id: Optional[int] = None
    media_type_id: Optional[int] = None
    genre_id: Optional[int] = None
    composer: Optional[str] = None
    milliseconds: Optional[int] = None
    bytes: Optional[int] = None
    unit_price: Optional[float] = None

    class Config:
        from_attributes = True
        populate_by_name = True


# -------- Used for response serialization (GET: /tracks/1) --------
class TrackRead(BaseModel):  # "flat read" - no joins
    track_id: int
    name: str
    album_id: Optional[int]
    media_type_id: int
    genre_id: Optional[int]
    composer: Optional[str]
    milliseconds: int
    bytes: Optional[int]
    unit_price: float

    class Config:
        from_attributes = True
        populate_by_name = True


# -------- Used for response serialization (GET: /albums/1) --------
# EXAMPLE OF A JOIN SCHEMA
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
