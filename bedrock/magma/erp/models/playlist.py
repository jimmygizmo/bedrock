from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from magma.core.database import Base


# ########    SQLALCHEMY MODEL:  playlist    ########



class Playlist(Base):
    __tablename__ = "playlists"

    playlist_id = Column("PlaylistId", Integer, primary_key=True, autoincrement=True)
    name = Column("Name", String(120))

    # * MANY-TO-MANY  (A special case, requiring an 'association table' or a 'many-to-many join table'.)
    # RELATIONSHIP - A 'playlist' is composed of multiple 'tracks' designed to be listened to together - AND ALSO,
    #   'tracks' or a 'track' can be on multiple 'playlists', especially if it is a popular track.
    # ---- Playlist (playlists) Many-to-many Track (tracks) - one track to many playlists AND one playlist to many tracks
    tracks = relationship("PlaylistTrack", back_populates="playlist")  # JOIN/ASSOC MODEL/TABLE: PlayListTrack


# --------  REFERENCE  --------
# NOTE: Bedrock does not use raw SQL for DB init. SQLAlchemy models are used. This SQL is only here for reference.
# CREATE TABLE playlist
# (
#     playlist_id INT NOT NULL GENERATED ALWAYS AS IDENTITY,
#     name VARCHAR(120),
#     CONSTRAINT playlist_pkey PRIMARY KEY  (playlist_id)
# );

