from pydantic import BaseModel, Field, field_validator, ConfigDict
from typing import Optional, List, TYPE_CHECKING
# from magma.schemas.genre import GenreRead
# from magma.schemas.media_type import MediaTypeRead
# from magma.schemas.invoice_line import InvoiceLineRead
# from magma.schemas.playlist_track import PlaylistTrackRead

# FIXES FOR CIRCULAR IMPORTS - MOVED TO END AFTER ALL DEFS:
# from magma.schemas.album import AlbumRead  # FOR OUR CIRCULAR IMPORT FIX, DO NOT IMPORT THIS HERE AT THE TOP
# if TYPE_CHECKING:
#     from magma.schemas.album import AlbumRead


# ########    PYDANTIC SCHEMA:  track    ########


# -------- Base schema shared across input/output --------
class TrackBase(BaseModel):
    name: str = Field(..., alias="Name")
    album_id: Optional[int] = Field(None, alias="AlbumId")
    media_type_id: int = Field(..., alias="MediaTypeId")
    genre_id: Optional[int] = Field(None, alias="GenreId")
    composer: Optional[str] = Field(None, alias="Composer")
    milliseconds: int = Field(..., alias="Milliseconds")
    bytes: Optional[int] = Field(None, alias="Bytes")
    unit_price: float = Field(..., alias="UnitPrice")

    class Config:
        from_attributes = True
        populate_by_name = True


# -------- Used for incoming POST data (POST: create a new track with new details) --------
class TrackCreate(TrackBase):

    # TODO: Enable this after ensuring our seed data is free of empty/no-value in this field.
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


# FIX ATTEMPT FOR CIRCULAR IMPORT
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
