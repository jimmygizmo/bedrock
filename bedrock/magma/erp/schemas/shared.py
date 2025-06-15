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

