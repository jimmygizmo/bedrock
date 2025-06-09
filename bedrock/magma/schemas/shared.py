from pydantic import BaseModel, Field
from typing import List


class AlbumRead(BaseModel):
    album_id: int = Field(alias="AlbumId")
    title: str = Field(alias="Title")

    class Config:
        from_attributes = True
        populate_by_name = True


class ArtistRead(BaseModel):
    artist_id: int = Field(alias="ArtistId")
    name: str
    albums: List[AlbumRead] = []

    class Config:
        from_attributes = True
        populate_by_name = True



# SQL CREATE from the original Chinook project for comparison with these Bedrock schemas

# CREATE TABLE album
# (
#     album_id INT NOT NULL GENERATED ALWAYS AS IDENTITY,
#     title VARCHAR(160) NOT NULL,
#     artist_id INT NOT NULL,
#     CONSTRAINT album_pkey PRIMARY KEY  (album_id)
# );

# CREATE TABLE artist
# (
#     artist_id INT NOT NULL GENERATED ALWAYS AS IDENTITY,
#     name VARCHAR(120),
#     CONSTRAINT artist_pkey PRIMARY KEY  (artist_id)
# );

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

# CREATE TABLE media_type
# (
#     media_type_id INT NOT NULL GENERATED ALWAYS AS IDENTITY,
#     name VARCHAR(120),
#     CONSTRAINT media_type_pkey PRIMARY KEY  (media_type_id)
# );

# CREATE TABLE genre
# (
#     genre_id INT NOT NULL GENERATED ALWAYS AS IDENTITY,
#     name VARCHAR(120),
#     CONSTRAINT genre_pkey PRIMARY KEY  (genre_id)
# );

