from fastapi import APIRouter, HTTPException
from magma.core.logger import log
from magma.core.dependencies import AsyncSessionDep
from magma.erp.schemas.track import TrackCreate, TrackUpdate, TrackRead
from magma.erp.services.track import *


# ########    ROUTER:  track    ########


router = APIRouter(prefix="/tracks", tags=["tracks"])


@router.get("/", response_model=list[TrackRead])
async def get_tracks(session: AsyncSessionDep, skip: int = 0, limit: int = 100):
    # log.info(f"📖>>>>>>>>    /tracks/    GET ALL (paged)")
    log.info(f"[[>>>>>>>>]]    /tracks/    GET ALL (paged)")  # TODO: ASCII vs. EMOJI ICON CONFIG OPTION COMING
    return await get_tracks_service(session, skip, limit)


# TODO: IMPORTANT FEATURE - CONTROL DETAIL LEVELS IN ENDPOINT OUTOUT - URL?detail=basic  vs.  URL?detail=full
# Example of how we would implement this in the router:
# @router.get("/users/", response_model=List[UserReadBasic])
# def list_users(detail: str = Query("basic")):
#     if detail == "full":
#         return user_service.get_users_full()
#     return user_service.get_users_basic()
# TODO: So we would have different services and different combinations of special READ schemas, likely residing in
#   models.erp.shared. The URL?param=value technique avoids excessive @router definitions and endpoint/API overgrowth.
#   Now it is also arguable that some special cases could deserve their own URL path or path component such as:
#   /resource/detailed/ but that needs to be carefully considered and would be hard to do while also being consistent
#   for your entire API if it is or will grow to being of any significant size.
#   The URL?param technique is growth-friendly, while using path components like /resource/detailed/ is growth-complex.
# THIS COMMENT IS REPEATED IN THE TRACK SCHEMA - CLEAN UP LATER AFTER IMPLEMENTING AT LEAST ONE EXAMPLE OF THIS.


@router.get("/{track_id}", response_model=TrackRead)
async def get_track(session: AsyncSessionDep, track_id: int):
    # log.info(f"📖>>>>    /tracks/{track_id}    GET SINGLE")
    log.info(f"[[>>>>]]    /tracks/{track_id}    GET SINGLE")  # TODO: ASCII vs. EMOJI ICON CONFIG OPTION COMING
    track = await get_track_service(session, track_id)
    if not track:
        raise HTTPException(status_code=404, detail="Track not found")
    return track


@router.post("/", response_model=TrackRead, status_code=201)
async def create_track(session: AsyncSessionDep, track_in: TrackCreate):
    # log.info(f"☘️++++    /tracks/    POST NEW")
    log.info(f"[[++++]]    /tracks/    POST NEW")  # TODO: ASCII vs. EMOJI ICON CONFIG OPTION COMING
    return await create_track_service(session, track_in)


@router.put("/{track_id}", response_model=TrackRead)
async def update_track(session: AsyncSessionDep, track_id: int, track_in: TrackUpdate):
    # log.info(f"✏️====    /tracks/{track_id}    PUT UPDATE")
    log.info(f"[[====]]    /tracks/{track_id}    PUT UPDATE")  # TODO: ASCII vs. EMOJI ICON CONFIG OPTION COMING
    track = await update_track_service(session, track_id, track_in)
    if not track:
        raise HTTPException(status_code=404, detail="Track not found")
    return track


@router.delete("/{track_id}", status_code=204)
async def delete_track(session: AsyncSessionDep, track_id: int):
    log.info(f"🗑️----    /tracks/{track_id}    DELETE")  # TODO: ASCII vs. EMOJI ICON CONFIG OPTION COMING
    log.info(f"[[----]]    /tracks/{track_id}    DELETE")
    success = await delete_track_service(session, track_id)
    if not success:
        raise HTTPException(status_code=404, detail="Track not found")

