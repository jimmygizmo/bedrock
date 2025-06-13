from fastapi import APIRouter, Depends, HTTPException
from magma.core.logger import log
from magma.core.dependencies import AsyncSessionDep
from magma.erp.schemas.media_type import MediaTypeCreate, MediaTypeUpdate, MediaTypeRead
from magma.erp.services.media_type import *


# ########    ROUTER:  media_type    ########


router = APIRouter(prefix="/media-types", tags=["media_types"])


@router.get("/", response_model=list[MediaTypeRead])
async def get_media_types(session: AsyncSessionDep, skip: int = 0, limit: int = 100):
    log.info(f"🧊  ----> /media-types/    GET ALL (paged)")
    return await get_media_types_service(session, skip, limit)


@router.get("/{media_type_id}", response_model=MediaTypeRead)
async def get_media_type(session: AsyncSessionDep, media_type_id: int):
    log.info(f"🧊  ----> /media-types/{media_type_id}    GET SINGLE")
    media_type = await get_media_type_service(session, media_type_id)
    if not media_type:
        raise HTTPException(status_code=404, detail="Media type not found")
    return media_type


@router.post("/", response_model=MediaTypeRead, status_code=201)
async def create_media_type(session: AsyncSessionDep, media_type_in: MediaTypeCreate):
    log.info(f"🧊  ----> /media-types/    POST NEW")
    return await create_media_type_service(session, media_type_in)


@router.put("/{media_type_id}", response_model=MediaTypeRead)
async def update_media_type(session: AsyncSessionDep, media_type_id: int, media_type_in: MediaTypeUpdate):
    log.info(f"🧊  ----> /media-types/{media_type_id}    PUT UPDATE")
    media_type = await update_media_type_service(session, media_type_id, media_type_in)
    if not media_type:
        raise HTTPException(status_code=404, detail="Media type not found")
    return media_type


@router.delete("/{media_type_id}", status_code=204)
async def delete_media_type(session: AsyncSessionDep, media_type_id: int):
    log.info(f"🧊  ----> /media-types/{media_type_id}    DELETE")
    success = await delete_media_type_service(session, media_type_id)
    if not success:
        raise HTTPException(status_code=404, detail="Media type not found")

