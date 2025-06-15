from fastapi import APIRouter, HTTPException
from magma.core.logger import log
from magma.core.dependencies import AsyncSessionDep
from magma.erp.schemas.playlist import PlaylistCreate, PlaylistUpdate, PlaylistRead
from magma.erp.services.playlist import *


# ########    ROUTER:  playlist    ########


router = APIRouter(prefix="/playlists", tags=["playlists"])


@router.get("/", response_model=list[PlaylistRead])
async def get_playlists(session: AsyncSessionDep, skip: int = 0, limit: int = 100):
    log.info("📖 >>>>    /playlists/    GET ALL")
    return await get_playlists_service(session, skip, limit)


@router.get("/{playlist_id}", response_model=PlaylistRead)
async def get_playlist(session: AsyncSessionDep, playlist_id: int):
    log.info(f"👁️ --->    /playlists/{playlist_id}    GET")
    playlist = await get_playlist_service(session, playlist_id)
    if not playlist:
        raise HTTPException(status_code=404, detail="Playlist not found")
    return playlist


@router.post("/", response_model=PlaylistRead, status_code=201)
async def create_playlist(session: AsyncSessionDep, playlist_in: PlaylistCreate):
    log.info("☘️ ++++    /playlists/    CREATE")
    return await create_playlist_service(session, playlist_in)


@router.put("/{playlist_id}", response_model=PlaylistRead)
async def update_playlist(session: AsyncSessionDep, playlist_id: int, playlist_in: PlaylistUpdate):
    log.info(f"✏️ ====    /playlists/{playlist_id}    UPDATE")
    playlist = await update_playlist_service(session, playlist_id, playlist_in)
    if not playlist:
        raise HTTPException(status_code=404, detail="Playlist not found")
    return playlist


@router.delete("/{playlist_id}", status_code=204)
async def delete_playlist(session: AsyncSessionDep, playlist_id: int):
    log.info(f"💥 ----    /playlists/{playlist_id}    DELETE")
    success = await delete_playlist_service(session, playlist_id)
    if not success:
        raise HTTPException(status_code=404, detail="Playlist not found")

