from fastapi import Depends
from fastapi import Header, HTTPException
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
import magma.core.config as cfg
from magma.core.logger import log
from magma.core.database import async_engine, Base


# ########    DEPENDENCIES - GLOBAL    ########


# TODO: Authentication dependencies would go here, for example.
# async def get_token_header(x_token: Annotated[str, Header()]):  # TODO: Rename
#     if x_token != "header-security-token-name":
#         raise HTTPException(status_code=400, detail="X-Token 'header-security-token-name' header invalid")
#
#
# async def get_query_token(token: str):  # TODO: Rename
#     if token != "security-token-name":
#         raise HTTPException(status_code=400, detail="No 'security-token-name' token provided")


async def get_db_async_session() -> AsyncSession:
    AsyncSessionLocal = async_sessionmaker(async_engine)
    db_async_session = AsyncSessionLocal()
    try:
        yield db_async_session
    finally:
        await db_async_session.close()


# Primary database session dependency
# AsyncSessionDep is used by all code accessing the DB. Called 'session' when used.
AsyncSessionDep = Annotated[AsyncSession, Depends(get_db_async_session)]

