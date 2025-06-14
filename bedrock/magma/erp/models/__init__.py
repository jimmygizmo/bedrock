"""
Centralized Model Initialization for ERP Module

This file is responsible for:
- Importing all model classes in dependency-safe order
- Defining inter-model SQLAlchemy relationships *after* all classes are loaded
- Avoiding circular import issues that can arise from defining relationships in-class
- Ensuring SQLAlchemy relationship mappings are finalized via `configure_mappers()`

IMPORTANT:
- Relationships such as `Album.artist` and `Artist.albums` are NOT defined in their class bodies.
  They are bound here using `sqlalchemy.orm.relationship` after all classes are imported.
- This is a strategic architectural choice to solve circular dependency issues cleanly.

DEVELOPER NOTES:
- Tools like PyCharm or linters may raise warnings about unresolved attributes on model classes.
  These can be safely ignored because the relationships *do* exist at runtime.
- To help with static analysis, consider adding `if TYPE_CHECKING:` stubs to model classes:

    ```python
    from typing import TYPE_CHECKING
    if TYPE_CHECKING:
        from magma.erp.models.artist import Artist

    class Album(Base):
        ...
        artist: "Artist"
    ```

- Always `import magma.erp.models` before accessing models to guarantee relationships are bound.
- Avoid re-defining relationships elsewhere — this module is the single source of truth.
"""
# This __init__.py is unique as it is designed to solve circular relationship and import order issues by getting all
# models imported before further defining certain relationships (involved in any circularity)
# TODO: Consolidate and re-write notes/comments above and below here.


from magma.erp.models.genre import Genre
from magma.erp.models.media_type import MediaType
from magma.erp.models.artist import Artist
from magma.erp.models.album import Album
from magma.erp.models.track import Track
from magma.erp.models.employee import Employee
from magma.erp.models.customer import Customer
from magma.erp.models.invoice import Invoice
from magma.erp.models.invoice_line import InvoiceLine
from magma.erp.models.playlist import Playlist
from magma.erp.models.playlist_track import PlaylistTrack

from sqlalchemy.orm import configure_mappers, relationship


# ########    LATE BINDINGS FOR FORWARD RELATIONSHIPS    ########


# Rebind forward relationships after all classes are loaded.
#
# This is an ideal strategy for large, circularly-dependent projects.
#
# NOTE: Always import magma.erp.models before using any of the models to guarantee relationship bindings happen.
# NOTE: Always eager-load relationships that will be accessed in the Pydantic response,
#       e.g. with selectinload(Album.artist).


# Genre ↔ Track(s)      (Genre is a dependency for Track)      (Many Tracks per Genre)
Track.genre = relationship("Genre", back_populates="tracks")
Genre.tracks = relationship("Track", back_populates="genre")

# MediaType ↔ Track(s)      (MediaType is a dependency for Track)      (Many Tracks per MediaType)
Track.media_type = relationship("MediaType", back_populates="tracks")
MediaType.tracks = relationship("Track", back_populates="media_type")


# Album(s) ↔ Artist
Artist.albums = relationship("Album", back_populates="artist")
Album.artist = relationship("Artist", back_populates="albums")

# Track(s) ↔ Album
Track.album = relationship("Album", back_populates="tracks")
Album.tracks = relationship("Track", back_populates="album")

# InvoiceLine(s) ↔ Track
Track.invoice_lines = relationship("InvoiceLine", back_populates="track")

# InvoiceLine(s) ↔ Invoice
Invoice.invoice_lines = relationship("InvoiceLine", back_populates="invoice")
InvoiceLine.invoice = relationship("Invoice", back_populates="invoice_lines")

# PlaylistTrack ↔ Playlist  (and Track)  * NOT LIKE THE OTHERS - TODO: Clarify in comments.
# TODO: RE comment above, decide if plural is appropriate. It would be:  # PlaylistTrack(s) ↔ Playlist   OK?
# ---- OPTIONAL COMMENTS TO USE (and does not show the plural (s) like that):
# PlaylistTrack ↔ Playlist (many PlaylistTracks per Playlist)
# NOTE: Naming is plural on Playlist.tracks to represent the *join* entities, not final Track objects.
Playlist.tracks = relationship("PlaylistTrack", back_populates="playlist")
PlaylistTrack.playlist = relationship("Playlist", back_populates="tracks")

# Playlist(s) ↔ Track
Track.playlists = relationship("PlaylistTrack", back_populates="track")
PlaylistTrack.track = relationship("Track", back_populates="playlists")


# Ensure mappers are fully configured
configure_mappers()


__all__ = [
    "Genre",
    "MediaType",
    "Artist",
    "Album",
    "Track",
    "Employee",
    "Customer",
    "Invoice",
    "InvoiceLine",
    "Playlist",
    "PlaylistTrack",
]


# -------- SCHEMA/DATA DEPENDENCY ORDER --------
# Based on relationships in our ERP/Chinook schema, this is the dependency order. We follow it for consistency even
# in contexts where the order is not important. This order matters most during data seeding but is determined by the
# structure of relationships.
#
# 1.   Genre
# 2.   MediaType
# 3.   Artist
# 4.   Album (depends on Artist)
# 5.   Track (depends on Album, Genre, MediaType)
# 6.   Employee (self-referencing for ReportsTo)
# 7.   Customer (depends on Employee via SupportRepId)
# 8.   Invoice (depends on Customer)
# 9.   InvoiceLine (depends on Invoice, Track)
# 10.  Playlist
# 11.  PlaylistTrack (depends on Playlist, Track)

