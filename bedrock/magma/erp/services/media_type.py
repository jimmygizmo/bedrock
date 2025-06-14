from sqlalchemy import select
from magma.core.dependencies import AsyncSessionDep
from fastapi import HTTPException
from magma.erp.models.media_type import MediaType
from magma.erp.schemas.media_type import MediaTypeCreate, MediaTypeUpdate
from typing import Optional, List


async def get_media_type_service(session: AsyncSessionDep, media_type_id: int) -> Optional[MediaType]:
    statement = select(MediaType).where(MediaType.media_type_id == media_type_id)
    result = await session.execute(statement)
    media_type = result.scalar_one_or_none()
    return media_type


async def get_media_types_service(session: AsyncSessionDep, skip: int = 0, limit: int = 10) -> List[MediaType]:
    statement = select(MediaType).offset(skip).limit(limit)
    result = await session.execute(statement)
    media_types = result.scalars().all()
    # TODO: In services/artist.py we had to force a similar return value to list() because PyCharm warned about the
    #   sequence type being returned. Why no similar issue here? Figure that out and maybe services/artist.py benefits.
    return media_types


# TODO: CHECK FOR NEEDING OUR FIXES
async def create_media_type_service(session: AsyncSessionDep, media_type_in: MediaTypeCreate) -> MediaType:
    media_type = MediaType(**media_type_in.model_dump())
    session.add(media_type)
    try:
        await session.commit()
        await session.refresh(media_type)
        return media_type
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=500, detail="Internal Server Error")


# TODO: CHECK FOR NEEDING OUR FIXES
async def update_media_type_service(session: AsyncSessionDep, media_type_id: int, media_type_in: MediaTypeUpdate) -> Optional[MediaType]:
    statement = select(MediaType).where(MediaType.media_type_id == media_type_id)
    result = await session.execute(statement)
    media_type = result.scalar_one_or_none()
    if not media_type:
        return None

    for field, value in media_type_in.model_dump(exclude_unset=True).items():
        setattr(media_type, field, value)

    await session.commit()
    await session.refresh(media_type)
    return media_type


async def delete_media_type_service(session: AsyncSessionDep, media_type_id: int) -> bool:
    statement = select(MediaType).where(MediaType.media_type_id == media_type_id)
    result = await session.execute(statement)
    media_type = result.scalar_one_or_none()
    if not media_type:
        return False

    await session.delete(media_type)
    await session.commit()
    return True
