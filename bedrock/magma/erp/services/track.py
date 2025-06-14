from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from magma.erp.models.track import Track
from magma.erp.schemas.track import TrackCreate, TrackUpdate


# ########    SERVICE:  track    ########


async def get_track_service(session: AsyncSession, track_id: int) -> Track | None:
    statement = (
        select(Track)
        .options(
            selectinload(Track.album),
            selectinload(Track.genre),
            selectinload(Track.media_type),
        )
        .where(Track.track_id == track_id)
    )
    result = await session.execute(statement)
    track = result.scalar_one_or_none()
    return track


async def get_tracks_service(session: AsyncSession, skip: int = 0, limit: int = 100) -> list[Track]:
    statement = (
        select(Track)
        .options(
            selectinload(Track.album),
            selectinload(Track.genre),
            selectinload(Track.media_type),
        )
        .offset(skip)
        .limit(limit)
    )
    result = await session.execute(statement)
    tracks = result.scalars().all()
    return list(tracks)


async def create_track_service(session: AsyncSession, track_in: TrackCreate) -> Track:
    track = Track(**track_in.model_dump())
    session.add(track)
    await session.commit()
    await session.refresh(track)
    return track


async def update_track_service(session: AsyncSession, track_id: int, track_in: TrackUpdate) -> Track | None:
    track = await get_track_service(session, track_id)
    if not track:
        return None

    for field, value in track_in.model_dump(exclude_unset=True).items():
        setattr(track, field, value)

    await session.commit()
    await session.refresh(track)
    return track


async def delete_track_service(session: AsyncSession, track_id: int) -> bool:
    track = await get_track_service(session, track_id)
    if not track:
        return False

    await session.delete(track)
    await session.commit()
    return True

