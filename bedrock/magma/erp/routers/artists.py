from fastapi import APIRouter, HTTPException
from magma.core.logger import log
from magma.core.dependencies import AsyncSessionDep
from magma.erp.schemas.artist import ArtistCreate, ArtistUpdate, ArtistRead
from magma.erp.services.artist import *


# ########    ROUTER:  artist    ########


router = APIRouter(prefix="/artists", tags=["artists"])


@router.get("/", response_model=list[ArtistRead])
async def get_artists(session: AsyncSessionDep, skip: int = 0, limit: int = 100):
    log.info(f"📖 >>>>    /artists/    GET ALL")
    return await get_artists_service(session, skip, limit)


@router.get("/{artist_id}", response_model=ArtistRead)
async def get_artist(session: AsyncSessionDep, artist_id: int):
    log.info(f"👁️ --->    /artists/{artist_id}     GET")
    artist = await get_artist_service(session, artist_id)
    if not artist:
        raise HTTPException(status_code=404, detail="Artist not found")
    return artist


@router.post("/", response_model=ArtistRead, status_code=201)
async def create_artist(session: AsyncSessionDep, artist_in: ArtistCreate):
    log.info(f"☘️ ++++    /artists/    CREATE")
    return await create_artist_service(session, artist_in)


@router.put("/{artist_id}", response_model=ArtistRead)
async def update_artist(session: AsyncSessionDep, artist_id: int, artist_in: ArtistUpdate):
    log.info(f"✏️ ====    /artists/{artist_id}    UPDATE")
    artist = await update_artist_service(session, artist_id, artist_in)
    if not artist:
        raise HTTPException(status_code=404, detail="Artist not found")
    return artist


@router.delete("/{artist_id}", status_code=204)
async def delete_artist(session: AsyncSessionDep, artist_id: int):
    log.info(f"️💥 ----    /artists/{artist_id}    DELETE")
    success = await delete_artist_service(session, artist_id)
    if not success:
        raise HTTPException(status_code=404, detail="Artist not found")

