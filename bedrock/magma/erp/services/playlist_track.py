from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from magma.erp.models.playlist_track import PlaylistTrack
from magma.erp.schemas.playlist_track import PlaylistTrackCreate, PlaylistTrackUpdate


# ########    SERVICE:  playlist_track    ########


async def get_playlist_track_service(session: AsyncSession, playlist_id: int, track_id: int) -> PlaylistTrack | None:
    statement = (
        select(PlaylistTrack)
        .options(selectinload(PlaylistTrack.playlist), selectinload(PlaylistTrack.track))
        .where(
            PlaylistTrack.playlist_id == playlist_id,
            PlaylistTrack.track_id == track_id
        )
    )
    result = await session.execute(statement)
    return result.scalar_one_or_none()


async def get_playlist_tracks_service(session: AsyncSession, skip: int = 0, limit: int = 100) -> list[PlaylistTrack]:
    statement = (
        select(PlaylistTrack)
        .options(
            selectinload(PlaylistTrack.playlist),
            selectinload(PlaylistTrack.track)
        ).offset(skip)
        .limit(limit)
    )
    result = await session.execute(statement)
    return list(result.scalars().all())


async def create_playlist_track_service(session: AsyncSession, playlist_track_in: PlaylistTrackCreate) -> PlaylistTrack:
    playlist_track = PlaylistTrack(**playlist_track_in.model_dump())
    session.add(playlist_track)
    await session.commit()
    await session.refresh(playlist_track)

    statement = (
        select(PlaylistTrack)
        .options(
            selectinload(PlaylistTrack.playlist),
            selectinload(PlaylistTrack.track)
        ).where(
            PlaylistTrack.playlist_id == playlist_track.playlist_id,
            PlaylistTrack.track_id == playlist_track.track_id
        )
    )
    result = await session.execute(statement)
    return result.scalar_one()


async def update_playlist_track_service(session: AsyncSession, playlist_id: int, track_id: int, playlist_track_in: PlaylistTrackUpdate) -> PlaylistTrack | None:
    playlist_track = await get_playlist_track_service(session, playlist_id, track_id)
    if not playlist_track:
        return None

    for field, value in playlist_track_in.model_dump(exclude_unset=True).items():
        setattr(playlist_track, field, value)

    await session.commit()
    await session.refresh(playlist_track)

    statement = (
        select(PlaylistTrack)
        .options(selectinload(PlaylistTrack.playlist), selectinload(PlaylistTrack.track))
        .where(
            PlaylistTrack.playlist_id == playlist_track.playlist_id,
            PlaylistTrack.track_id == playlist_track.track_id
        )
    )
    result = await session.execute(statement)
    return result.scalar_one()


async def delete_playlist_track_service(session: AsyncSession, playlist_id: int, track_id: int) -> bool:
    playlist_track = await get_playlist_track_service(session, playlist_id, track_id)
    if not playlist_track:
        return False

    await session.delete(playlist_track)
    await session.commit()
    return True

