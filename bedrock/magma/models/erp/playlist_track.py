from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from magma.core.database import Base


# ########    SQLALCHEMY MODEL:  playlist_tracks    ########

# SPECIAL MODEL:  ASSOCIATION TABLE / MANY-TO-MANY JOIN TABLE
# RELATIONSHIPS - A 'track' will be in multiple 'playlists' especially if it is a popular 'track' - AND ALSO,
#   'playlists' are of course composed of multiple 'tracks'.


class PlaylistTrack(Base):
    __tablename__ = "playlist_tracks"

    playlist_id = Column("PlaylistId", Integer, ForeignKey("playlists.PlaylistId"), primary_key=True)
    track_id = Column("TrackId", Integer, ForeignKey("tracks.TrackId"), primary_key=True)

    # RELATIONSHIP - Many 'playlist_tracks' will be on a single 'playlist' for them to be listened to together:
    # ---- PlaylistTrack Many-to-one Playlist (playlists) - many playlist_tracks to one playlist
    playlist = relationship("Playlist", back_populates="tracks")

    # * THIS ASSOCIATION TABLE JOINS TRACKS TO PLAYLISTS IN A MANY-TO-MANY RELATIONSHIP

    # RELATIONSHIP - Many 'playlists' can have the same 'track' on them, especially if that track is popular:
    # ---- PlaylistTrack Many-to-one Track (tracks) - many playlists to one track
    track = relationship("Track", back_populates="playlists")


# SQL CREATE from the original Chinook project for comparison with this Bedrock model
#
# CREATE TABLE playlist_track
# (
#     playlist_id INT NOT NULL,
#     track_id INT NOT NULL,
#     CONSTRAINT playlist_track_pkey PRIMARY KEY  (playlist_id, track_id)
# );

