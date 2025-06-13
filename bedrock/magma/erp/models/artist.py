from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from magma.core.database import Base


# ########    SQLALCHEMY MODEL:  artist    ########


class Artist(Base):
    __tablename__ = "artists"

    artist_id = Column("ArtistId", Integer, primary_key=True, autoincrement=True)
    name = Column("Name", String(120))

    # RELATIONSHIP - An 'artist' can have many 'albums' they have released over the years:
    # ---- Artist One-to-many Album (albums) - one artist to many albums
    albums = relationship("Album", back_populates="artist")


# --------  REFERENCE  --------
# NOTE: Bedrock does not use raw SQL for DB init. SQLAlchemy models are used. This SQL is only here for reference.
# CREATE TABLE artist
# (
#     artist_id INT NOT NULL GENERATED ALWAYS AS IDENTITY,
#     name VARCHAR(120),
#     CONSTRAINT artist_pkey PRIMARY KEY  (artist_id)
# );

