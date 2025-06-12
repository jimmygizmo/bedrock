from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from magma.core.database import Base


# ########    SQLALCHEMY MODEL:  genre    ########


class Genre(Base):
    __tablename__ = "genres"

    genre_id = Column("GenreId", Integer, primary_key=True, autoincrement=True)
    name = Column("Name", String(120))

    # RELATIONSHIP - A 'genre' has many/numerous 'tracks' which are all tagged as being members of that 'genre':
    # ---- Genre One-to-many Track (tracks) - one genre to many tracks
    tracks = relationship("Track", back_populates="genre")


# --------  REFERENCE  --------
# SQL CREATE from the original Chinook project
#
# CREATE TABLE genre
# (
#     genre_id INT NOT NULL GENERATED ALWAYS AS IDENTITY,
#     name VARCHAR(120),
#     CONSTRAINT genre_pkey PRIMARY KEY  (genre_id)
# );

