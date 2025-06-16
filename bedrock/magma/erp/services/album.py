from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload, joinedload

from magma.erp.models.album import Album
from magma.erp.models.track import Track
from magma.erp.schemas.album import AlbumCreate, AlbumUpdate

# For temporary examination of the raw SQL from select() statements
from sqlalchemy.dialects import postgresql
import magma.core.config as cfg
from magma.core.logger import log


# ########    SERVICE:  album    ########


async def get_album_service(session: AsyncSession, album_id: int) -> Album | None:
    if cfg.db_join_optimize:  # STRATEGY;    JOINEDLOAD - Do the work on the DB in one big query
        statement = (
            select(Album)
            .options(
                joinedload(Album.artist),
                joinedload(Album.tracks).joinedload(Track.genre),
                joinedload(Album.tracks).joinedload(Track.media_type),
            )
            .where(Album.album_id == album_id)
        )
        # Logging raw SQL as joinedload is being experimentally compared to selecinload for performance
        raw_sql = statement.compile(dialect=postgresql.dialect(), compile_kwargs={"literal_binds": True})
        log.debug(f"- - - - - - - - -  RAW SQL  - - - - - - - - -")
        log.debug(f"{raw_sql}")
        log.debug(f"- - - - - - - - - - - - - - - - - - - - - - -")
        result = await session.execute(statement)
        album = result.unique().scalar_one_or_none()  # Joinedload must use result.unique()
        return album
    else:  # STRATEGY:    SELECTINLOAD - Do the work in Python with lots of smaller queries
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
        album = result.scalar_one_or_none()  # Selectinload does not use the unique method.
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

