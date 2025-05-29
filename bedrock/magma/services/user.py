from sqlalchemy import select
from magma.models.user import User
from magma.schemas.user import UserCreate
from magma.core.dependencies import AsyncSessionDep  # TODO: This may become magma.core.dependencies
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError


# ########    SERVICE:  user    ########


async def create_user(session: AsyncSessionDep, user: UserCreate) -> User:
    new_user = User(**user.model_dump())  # Updated for Pydantic v2
    session.add(new_user)  # Synchronous - no await
    try:
        await session.commit()
        await session.refresh(new_user)
        return new_user
    except IntegrityError as e:
        await session.rollback()
        raise HTTPException(status_code=400, detail="User with this email already exists.")
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=500, detail="Internal Server Error")


async def get_user(session: AsyncSessionDep, user_id: int):
    statement = select(User).where(User.id == user_id)
    result = await session.execute(statement)
    found_user = result.scalar_one_or_none()
    return found_user


async def get_users(session: AsyncSessionDep, skip: int = 0, limit: int = 10):
    stmt = select(User).offset(skip).limit(limit)
    result = await session.execute(stmt)
    users = result.scalars().all()
    return users

