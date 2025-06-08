from sqlalchemy import Column, ForeignKey, Integer, String, Numeric
from sqlalchemy.orm import relationship
from magma.core.database import Base


# ########    SQLALCHEMY MODEL:  track    ########


class Track(Base):
    __tablename__ = "tracks"

    track_id = Column("TrackId", Integer, primary_key=True, autoincrement=True)
    name = Column("Name", String(200), nullable=False)
    album_id = Column("AlbumId", Integer, ForeignKey("albums.album_id"))
    media_type_id = Column("MediaTypeId", Integer, ForeignKey("media_types.media_type_id"), nullable=False)
    genre_id = Column("GenreId", Integer, ForeignKey("genres.genre_id"))
    composer = Column("Composer", String(220))
    milliseconds = Column("Milliseconds", Integer, nullable=False)
    bytes = Column("Bytes", Integer)
    unit_price = Column("UnitPrice", Numeric(10, 2), nullable=False)

    # RELATIONSHIP - Many 'tracks' can be on a single 'album' with the average number being around 10-14:
    # ---- Track Many-to-one Album (album) - many tracks to one album
    album = relationship("Album", back_populates="tracks")

    # RELATIONSHIP - Many/numerous 'tracks' can be members of a single 'media_type':
    # ---- Track Many-to-one MediaType (media_type) - many tracks to one media_type
    media_type = relationship("MediaType", back_populates="tracks")

    # RELATIONSHIP - Many/numerous 'tracks' can be members of a single 'genre':
    # ---- Track Many-to-one Genre (genre) - many tracks to one genre
    genre = relationship("Genre", back_populates="tracks")

    # RELATIONSHIP - A 'track' will be in multiple 'invoice_lines' because multiple copies of tracks are sold:
    # ---- Track One-to-many InvoiceLines (invoice_lines) - one track to many invoice_lines
    invoice_lines = relationship("InvoiceLine", back_populates="track")

    # * MANY-TO-MANY  (A special case, requiring an 'association table' or a 'many-to-many join table'.)
    # RELATIONSHIP - A 'track' will be in multiple 'playlists' espeically if it is a popular 'track' - AND ALSO,
    #   'playlists' are of course composed of multiple 'tracks'.
    # ---- Track (tracks) Many-to-many Playlist (playlists) - one track to many playlists AND one playlist to many tracks
    playlists = relationship("PlaylistTrack", back_populates="track")  # JOIN/ASSOC MODEL/TABLE: PlayListTrack


# SQL CREATE from the original Chinook project for comparison with this Bedrock model
#
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

