from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from magma.erp.models.album import Album
from magma.erp.models.track import Track
from magma.erp.schemas.album import AlbumCreate, AlbumUpdate


# ########    SERVICE:  album    ########


# TODO: Add this to formal docs:
# ***  HOW TO FIGURE OUT WHEN YOU NEED THE EAGER LOADING FROM selecinload - AND WHAT YOU NEED TO EAGER LOAD  ***
# NOTE: AlbumRead includes these:
#     artist: ArtistSimpleRead
#                 class ArtistSimpleRead(ConfigBase):
#                     artist_id: int = Field(alias="ArtistId")
#                     name: str = Field(alias="Name")
#     tracks: list[TrackSimpleRead]
#                 class TrackSimpleRead(ConfigBase):
#                     track_id: int
#                     name: str
#                     media_type: Optional[MediaTypeRead]
#                     genre: Optional[GenreRead]
#                    ... other flat metadata fields ...
#
# **** HENCE - AlbumRead UNDER ASYNC ALWAYS REQUIRES:
#             selectinload(Album.artist),
#             selectinload(Album.tracks).selectinload(Track.genre),
#             selectinload(Album.tracks).selectinload(Track.media_type),


async def get_album_service(session: AsyncSession, album_id: int) -> Album | None:
    statement = (
        select(Album)
        .options(
            selectinload(Album.artist),
            selectinload(Album.tracks).selectinload(Track.genre),
            selectinload(Album.tracks).selectinload(Track.media_type),
        )
        .where(Album.album_id == album_id)
    )
    result = await session.execute(statement)
    album = result.scalar_one_or_none()
    return album


async def get_albums_service(session: AsyncSession, skip: int = 0, limit: int = 100) -> list[Album]:
    statement = (
        select(Album)
        .options(
            selectinload(Album.artist),
            selectinload(Album.tracks).selectinload(Track.genre),
            selectinload(Album.tracks).selectinload(Track.media_type),
        )
        .offset(skip)
        .limit(limit)
    )
    result = await session.execute(statement)
    albums = result.scalars().all()
    return list(albums)  # list() here does nothing but does suppress false static type warnings


async def create_album_service(session: AsyncSession, album_in: AlbumCreate) -> Album:
    album = Album(**album_in.model_dump())
    session.add(album)
    await session.commit()
    await session.refresh(album)
    statement = (
        select(Album)
        .options(
            selectinload(Album.artist),
            selectinload(Album.tracks),
        )
        .where(Album.album_id == album.album_id)
    )
    result = await session.execute(statement)
    album_with_rels = result.scalar_one()
    return album_with_rels


async def update_album_service(session: AsyncSession, album_id: int, album_in: AlbumUpdate) -> Album | None:
    album = await get_album_service(session, album_id)
    if not album:
        return None
    for field, value in album_in.model_dump(exclude_unset=True).items():
        setattr(album, field, value)
    await session.commit()
    await session.refresh(album)
    statement = (
        select(Album)
        .options(
            selectinload(Album.artist),
            selectinload(Album.tracks),
        )
        .where(Album.album_id == album.album_id)
    )
    result = await session.execute(statement)
    album_with_rels = result.scalar_one()
    return album_with_rels


async def delete_album_service(session: AsyncSession, album_id: int) -> bool:
    album = await get_album_service(session, album_id)
    if not album:
        return False

    await session.delete(album)
    await session.commit()
    return True

