from fastapi import APIRouter, Depends, HTTPException
from magma.core.logger import log
from magma.core.dependencies import AsyncSessionDep
from magma.erp.schemas.album import AlbumCreate, AlbumUpdate, AlbumRead
from magma.erp.services.album import *


# ########    ROUTER:  album    ########


router = APIRouter(prefix="/albums", tags=["albums"])


@router.get("/", response_model=list[AlbumRead])
async def get_albums(session: AsyncSessionDep, skip: int = 0, limit: int = 100):
    log.info(f"🧊  ----> /albums/    GET ALL (paged)")
    return await get_albums_service(session, skip, limit)


@router.get("/{album_id}", response_model=AlbumRead)
async def get_album(session: AsyncSessionDep, album_id: int):
    log.info(f"🧊  ----> /albums/{album_id}    GET SINGLE")
    album = await get_album_service(session, album_id)
    if not album:
        raise HTTPException(status_code=404, detail="Album not found")
    return album


@router.post("/", response_model=AlbumRead, status_code=201)
async def create_album(session: AsyncSessionDep, album_in: AlbumCreate):
    log.info(f"🧊  ----> /albums/    POST NEW")
    return await create_album_service(session, album_in)


@router.put("/{album_id}", response_model=AlbumRead)
async def update_album(session: AsyncSessionDep, album_id: int, album_in: AlbumUpdate):
    log.info(f"🧊  ----> /albums/{album_id}    PUT UPDATE")
    album = await update_album_service(session, album_id, album_in)
    if not album:
        raise HTTPException(status_code=404, detail="Album not found")
    return album


@router.delete("/{album_id}", status_code=204)
async def delete_album(session: AsyncSessionDep, album_id: int):
    log.info(f"🧊  ----> /albums/{album_id}    DELETE")
    success = await delete_album_service(session, album_id)
    if not success:
        raise HTTPException(status_code=404, detail="Album not found")

