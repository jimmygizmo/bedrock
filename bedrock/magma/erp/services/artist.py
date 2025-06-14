from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from sqlalchemy.exc import NoResultFound

from magma.erp.models.artist import Artist
from magma.erp.schemas.artist import ArtistCreate, ArtistUpdate


# ########    SERVICE:  artist    ########


async def get_artist_service(session: AsyncSession, artist_id: int) -> Artist | None:
    statement = select(Artist).where(Artist.artist_id == artist_id)
    result = await session.execute(statement)
    artist = result.scalar_one_or_none()
    return artist


async def get_artists_service(session: AsyncSession, skip: int = 0, limit: int = 100) -> list[Artist]:
    # statement = select(Artist).offset(skip).limit(limit)
    # TODO: FIX: We must eagerly load the related records, particularly in an ASYNC context:
    statement = (
        select(Artist)
        .options(selectinload(Artist.albums))
        .offset(skip)
        .limit(limit)
    )
    result = await session.execute(statement)
    artists =  result.scalars().all()
    # TODO: Figure out why we need to force this sequence to a list before returning in this one? Seems like other
    #   endpoint would have a similar issue. Update comments later with explanation of a consistent solution.
    #   UPDATE: The response models are different and artists includes related albums so that could be related to the
    #   issue as the response model for genre read is a simple list and that one does not need coercing like this one.
    return list(artists)


async def create_artist_service(session: AsyncSession, artist_in: ArtistCreate) -> Artist:
    artist = Artist(**artist_in.model_dump())
    session.add(artist)
    await session.commit()
    await session.refresh(artist)
    return artist


async def update_artist_service(session: AsyncSession, artist_id: int, artist_in: ArtistUpdate) -> Artist | None:
    artist = await get_artist_service(session, artist_id)
    if not artist:
        return None

    for field, value in artist_in.model_dump(exclude_unset=True).items():
        setattr(artist, field, value)

    await session.commit()
    await session.refresh(artist)
    return artist


async def delete_artist_service(session: AsyncSession, artist_id: int) -> bool:
    artist = await get_artist_service(session, artist_id)
    if not artist:
        return False

    await session.delete(artist)
    await session.commit()
    return True
