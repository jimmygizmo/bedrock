from fastapi import APIRouter, HTTPException
from magma.core.logger import log
from magma.schemas.user import UserCreate, UserRead
from magma.services.user import create_user, get_user, get_users
from magma.core.dependencies import AsyncSessionDep  # TODO: This may become magma.core.dependencies


router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=UserRead)
async def create_new_user(session: AsyncSessionDep, user: UserCreate):
    log.info(f"🧊  ----> /users/    POST NEW")
    return await create_user(session, user)


@router.get("/{user_id}", response_model=UserRead)
async def read_user(session: AsyncSessionDep, user_id: int):
    log.info(f"🧊  ----> /users/{user_id}")
    one_user = await get_user(session, user_id)
    if one_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return one_user


@router.get("/", response_model=list[UserRead])
async def read_users(session: AsyncSessionDep, skip: int = 0, limit: int = 10):
    log.info(f"🧊  ----> /users/")
    return await get_users(session, skip=skip, limit=limit)

