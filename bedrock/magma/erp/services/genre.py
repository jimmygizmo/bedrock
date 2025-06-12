from sqlalchemy import select
from magma.core.dependencies import AsyncSessionDep
from fastapi import HTTPException
from magma.erp.models.genre import Genre
from magma.erp.schemas.genre import GenreCreate, GenreUpdate
from typing import Optional, List


async def get_genre(session: AsyncSessionDep, genre_id: int) -> Optional[Genre]:
    statement = select(Genre).where(Genre.genre_id == genre_id)
    result = await session.execute(statement)
    found_genre = result.scalar_one_or_none()
    return found_genre


async def get_genres(session: AsyncSessionDep, skip: int = 0, limit: int = 10) -> List[Genre]:
    statement = select(Genre).offset(skip).limit(limit)
    result = await session.execute(statement)
    genres = result.scalars().all()
    return genres


async def create_genre(session: AsyncSessionDep, genre_in: GenreCreate) -> Genre:
    genre = Genre(**genre_in.model_dump(by_alias=True))
    session.add(genre)
    try:
        await session.commit()
        await session.refresh(genre)
        return genre
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=500, detail="Internal Server Error")
    # except IntegrityError as e:  # EXAMPLE: FOR COLUMNS MARKED AS UNIQUE AND POSSIBLY OTHER INTEGRITY CRITERIA
    #     await session.rollback()
    #     raise HTTPException(status_code=400, detail="User with this email already exists.")


async def update_genre(session: AsyncSessionDep, genre_id: int, genre_in: GenreUpdate) -> Optional[Genre]:
    statement = select(Genre).where(Genre.genre_id == genre_id)
    result = await session.execute(statement)
    genre = result.scalar_one_or_none()
    if not genre:
        return None

    for field, value in genre_in.model_dump(exclude_unset=True, by_alias=True).items():
        setattr(genre, field, value)

    await session.commit()
    await session.refresh(genre)
    return genre


async def delete_genre(session: AsyncSessionDep, genre_id: int) -> bool:
    statement = select(Genre).where(Genre.genre_id == genre_id)
    result = await session.execute(statement)
    genre = result.scalar_one_or_none()
    if not genre:
        return False

    await session.delete(genre)
    await session.commit()
    return True

