from fastapi import APIRouter, HTTPException
from magma.core.logger import log
from magma.core.dependencies import AsyncSessionDep
from magma.erp.schemas.playlist_track import PlaylistTrackCreate, PlaylistTrackUpdate, PlaylistTrackRead
from magma.erp.services.playlist_track import *


# ########    ROUTER:  playlist_track    ########


router = APIRouter(prefix="/playlist-tracks", tags=["playlist_tracks"])


@router.get("/", response_model=list[PlaylistTrackRead])
async def get_playlist_tracks(session: AsyncSessionDep, skip: int = 0, limit: int = 100):
    log.info("📖 >>>>    /playlist-tracks/    GET ALL")
    return await get_playlist_tracks_service(session, skip, limit)


@router.get("/{playlist_id}/{track_id}", response_model=PlaylistTrackRead)
async def get_playlist_track(session: AsyncSessionDep, playlist_id: int, track_id: int):
    log.info(f"👁️ --->    /playlist-tracks/{playlist_id}/{track_id}    GET")
    playlist_track = await get_playlist_track_service(session, playlist_id, track_id)
    if not playlist_track:
        raise HTTPException(status_code=404, detail="PlaylistTrack not found")
    return playlist_track


@router.post("/", response_model=PlaylistTrackRead, status_code=201)
async def create_playlist_track(session: AsyncSessionDep, playlist_track_in: PlaylistTrackCreate):
    log.info("☘️ ++++    /playlist-tracks/    CREATE")
    return await create_playlist_track_service(session, playlist_track_in)


@router.put("/{playlist_id}/{track_id}", response_model=PlaylistTrackRead)
async def update_playlist_track(session: AsyncSessionDep, playlist_id: int, track_id: int, playlist_track_in: PlaylistTrackUpdate):
    log.info(f"✏️ ====    /playlist-tracks/{playlist_id}/{track_id}    UPDATE")
    playlist_track = await update_playlist_track_service(session, playlist_id, track_id, playlist_track_in)
    if not playlist_track:
        raise HTTPException(status_code=404, detail="PlaylistTrack not found")
    return playlist_track


@router.delete("/{playlist_id}/{track_id}", status_code=204)
async def delete_playlist_track(session: AsyncSessionDep, playlist_id: int, track_id: int):
    log.info(f"💥 ----    /playlist-tracks/{playlist_id}/{track_id}    DELETE")
    success = await delete_playlist_track_service(session, playlist_id, track_id)
    if not success:
        raise HTTPException(status_code=404, detail="PlaylistTrack not found")

