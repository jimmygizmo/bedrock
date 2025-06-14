from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from magma.erp.models.album import Album
from magma.erp.models.track import Track
from magma.erp.schemas.album import AlbumCreate, AlbumUpdate


# ########    SERVICE:  album    ########


async def get_album_service(session: AsyncSession, album_id: int) -> Album | None:
    statement = (
        select(Album)
        .options(
            selectinload(Album.artist),
            selectinload(Album.tracks),
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
    return list(albums)


async def create_album_service(session: AsyncSession, album_in: AlbumCreate) -> Album:
    album = Album(**album_in.model_dump())
    session.add(album)
    await session.commit()
    await session.refresh(album)
    return album


async def update_album_service(session: AsyncSession, album_id: int, album_in: AlbumUpdate) -> Album | None:
    album = await get_album_service(session, album_id)
    if not album:
        return None

    for field, value in album_in.model_dump(exclude_unset=True).items():
        setattr(album, field, value)

    await session.commit()
    await session.refresh(album)
    return album


async def delete_album_service(session: AsyncSession, album_id: int) -> bool:
    album = await get_album_service(session, album_id)
    if not album:
        return False

    await session.delete(album)
    await session.commit()
    return True

