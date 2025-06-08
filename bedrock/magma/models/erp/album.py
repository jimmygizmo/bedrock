from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from magma.core.database import Base


# ########    SQLALCHEMY MODEL:  album    ########


class Album(Base):
    __tablename__ = "albums"

    album_id = Column("AlbumId", Integer, primary_key=True, autoincrement=True)
    title = Column("Title", String(160), nullable=False)
    artist_id = Column("ArtistId", Integer, ForeignKey("artists.artist_id"), nullable=False)

    # RELATIONSHIP - Many 'albums' can come from a single 'artist':
    # ---- Album Many-to-one Artist (artists) - many albums to one artist
    artist = relationship("Artist", back_populates="albums")

    # RELATIONSHIP - An 'album' usually has multiple 'tracks' with the average being around 10-14 'tracks':
    # ---- Album One-to-many Track (tracks) - one album to many tracks
    tracks = relationship("Track", back_populates="album")


# SQL CREATE from the original Chinook project for comparison with this Bedrock model
#
# CREATE TABLE album
# (
#     album_id INT NOT NULL GENERATED ALWAYS AS IDENTITY,
#     title VARCHAR(160) NOT NULL,
#     artist_id INT NOT NULL,
#     CONSTRAINT album_pkey PRIMARY KEY  (album_id)
# );

