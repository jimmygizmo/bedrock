from pydantic import BaseModel, Field
from typing import List, Optional
from magma.erp.schemas.media_type import MediaTypeRead
from magma.erp.schemas.genre import GenreRead


# ########    PYDANTIC SCHEMA:  shared    ########


# --------  CONFIG  --------
class ConfigBase(BaseModel):
    model_config = {
        "from_attributes": True,
        "populate_by_name": True,
    }


# --------  READ RELATED  --------
class AlbumRead(ConfigBase):
    album_id: int = Field(alias="AlbumId")
    title: str = Field(alias="Title")


# --------  READ RELATED  --------
class ArtistRead(ConfigBase):
    artist_id: int = Field(alias="ArtistId")
    name: str = Field(alias="Name")
    albums: List[AlbumRead] = []


# --------  READ RELATED  --------
class ArtistSimpleRead(ConfigBase):
    artist_id: int = Field(alias="ArtistId")
    name: str = Field(alias="Name")


# --------  READ RELATED  --------
# TODO: Alternate naming idea: TrackReadForAlbumView
class TrackSimpleRead(ConfigBase):
    track_id: int
    name: str
    media_type: Optional[MediaTypeRead]
    genre: Optional[GenreRead]
    composer: Optional[str]
    milliseconds: int
    bytes: Optional[int]
    unit_price: float
# TODO: THis is an improvement but we should flatten MediaTypeRead and GenreRead so we just get the names and not
#    a structure including the id for MediaType and Genre.


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

