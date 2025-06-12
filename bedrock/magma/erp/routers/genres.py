from fastapi import APIRouter, Depends, HTTPException
from magma.core.logger import log
from magma.core.dependencies import AsyncSessionDep
from magma.erp.schemas.genre import GenreCreate, GenreUpdate, GenreRead
from magma.erp.services.genre import *


# ########    ROUTER:  genre    ########


router = APIRouter(prefix="/genres", tags=["genres"])


@router.get("/", response_model=list[GenreRead])
async def read_genres(session: AsyncSessionDep, skip: int = 0, limit: int = 100):
    log.info(f"🧊  ----> /genres/    GET ALL (paged)")
    return await get_genres(session, skip, limit)


@router.get("/{genre_id}", response_model=GenreRead)
async def read_genre(session: AsyncSessionDep, genre_id: int):
    log.info(f"🧊  ----> /genres/{genre_id}    GET SINGLE")
    genre = await get_genre(session, genre_id)
    if not genre:
        raise HTTPException(status_code=404, detail="Genre not found")
    return genre


@router.post("/", response_model=GenreRead, status_code=201)
async def create_new_genre(session: AsyncSessionDep, genre_in: GenreCreate):
    log.info(f"🧊  ----> /genres/    POST NEW")
    return await create_genre(session, genre_in)


@router.put("/{genre_id}", response_model=GenreRead)
async def update_existing_genre(session: AsyncSessionDep, genre_id: int, genre_in: GenreUpdate):
    log.info(f"🧊  ----> /genres/{genre_id}    PUT UPDATE")
    genre = await update_genre(session, genre_id, genre_in)
    if not genre:
        raise HTTPException(status_code=404, detail="Genre not found")
    return genre


@router.delete("/{genre_id}", status_code=204)
async def delete_existing_genre(session: AsyncSessionDep, genre_id: int):
    log.info(f"🧊  ----> /genres/{genre_id}    DELETE")
    success = await delete_genre(session, genre_id)
    if not success:
        raise HTTPException(status_code=404, detail="Genre not found")

