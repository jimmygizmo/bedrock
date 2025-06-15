from fastapi import APIRouter, HTTPException
from magma.core.logger import log
from magma.schemas.user import UserCreate, UserRead
from magma.core.dependencies import AsyncSessionDep
from magma.services.user import get_user_service, get_users_service, create_user_service


# ########    ROUTER:  user    ########


router = APIRouter(prefix="/users", tags=["users"])


@router.get("/", response_model=list[UserRead])
async def get_users(session: AsyncSessionDep, skip: int = 0, limit: int = 10):
    log.info(f"📖 >>>>    /users/    GET ALL")
    return await get_users_service(session, skip=skip, limit=limit)


@router.get("/{user_id}", response_model=UserRead)
async def get_user(session: AsyncSessionDep, user_id: int):
    log.info(f"👁️ --->    /users/{user_id}    GET")
    one_user = await get_user_service(session, user_id)
    if one_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return one_user


@router.post("/", response_model=UserRead)
async def create_new_user(session: AsyncSessionDep, user: UserCreate):
    log.info(f"☘️ ++++    /users/    CREATE")
    return await create_user_service(session, user)


# TODO: Add delete handler and service method

