from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from magma.erp.models.playlist import Playlist
from magma.erp.schemas.playlist import PlaylistCreate, PlaylistUpdate


# ########    SERVICE:  playlist    ########


async def get_playlist_service(session: AsyncSession, playlist_id: int) -> Playlist | None:
    statement = select(Playlist).where(Playlist.playlist_id == playlist_id)
    result = await session.execute(statement)
    return result.scalar_one_or_none()


async def get_playlists_service(session: AsyncSession, skip: int = 0, limit: int = 100) -> list[Playlist]:
    statement = select(Playlist).offset(skip).limit(limit)
    result = await session.execute(statement)
    return list(result.scalars().all())


# async def create_playlist_service(session: AsyncSession, playlist_in: PlaylistCreate) -> Playlist:
#     playlist = Playlist(**playlist_in.model_dump())
#     session.add(playlist)
#     await session.commit()
#     await session.refresh(playlist)
#
#     statement = select(Playlist).where(Playlist.playlist_id == playlist.playlist_id)
#     result = await session.execute(statement)
#     return result.scalar_one()

async def create_playlist_service(session: AsyncSession, playlist_in: PlaylistCreate) -> Playlist:
    playlist = Playlist(**playlist_in.model_dump())
    session.add(playlist)
    await session.commit()
    await session.refresh(playlist)

    statement = (
        select(Playlist)
        .options(selectinload(Playlist.tracks))
        .where(Playlist.playlist_id == playlist.playlist_id)
    )
    result = await session.execute(statement)
    playlist_with_rels = result.scalar_one()

    return playlist_with_rels


# async def update_playlist_service(session: AsyncSession, playlist_id: int, playlist_in: PlaylistUpdate) -> Playlist | None:
#     playlist = await get_playlist_service(session, playlist_id)
#     if not playlist:
#         return None
#
#     for field, value in playlist_in.model_dump(exclude_unset=True).items():
#         setattr(playlist, field, value)
#
#     await session.commit()
#     await session.refresh(playlist)
#     return playlist


async def update_playlist_service(session: AsyncSession, playlist_id: int, playlist_in: PlaylistUpdate) -> Playlist | None:
    playlist = await get_playlist_service(session, playlist_id)
    if not playlist:
        return None

    for field, value in playlist_in.model_dump(exclude_unset=True).items():
        setattr(playlist, field, value)

    await session.commit()
    await session.refresh(playlist)

    statement = (
        select(Playlist)
        .options(selectinload(Playlist.tracks))
        .where(Playlist.playlist_id == playlist.playlist_id)
    )
    result = await session.execute(statement)
    playlist_with_rels = result.scalar_one()

    return playlist_with_rels


async def delete_playlist_service(session: AsyncSession, playlist_id: int) -> bool:
    playlist = await get_playlist_service(session, playlist_id)
    if not playlist:
        return False

    await session.delete(playlist)
    await session.commit()
    return True

