from httpx import AsyncClient
import asyncio
import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from magma.core.database import Base
import magma.core.config as cfg
# from magma.core.config import DATABASE_URL

# TODO: We need a cfg.DEV_STACK_DATABASE_URL or equivalent.
DEV_STACK_DATABASE_URL: str = f"postgresql+asyncpg://bedrock:bedrock@localhost:45432/bedrockdb"


@pytest_asyncio.fixture
async def async_http_client():
    """Real network client to running FastAPI service on port 48000."""
    async with AsyncClient(base_url="http://localhost:48000") as client:
        yield client



# Create engine and session factory directly for testing
test_engine = create_async_engine(
    DEV_STACK_DATABASE_URL,
    echo=True,
    future=True,
    pool_size=20,
    max_overflow=30
)
# test_engine = create_async_engine(
#     DEV_STACK_DATABASE_URL,
#     echo=True,
#     # future=True,
#     # pool_size=20,
#     # max_overflow=30,
# )
TestAsyncSessionLocal = async_sessionmaker(bind=test_engine, expire_on_commit=False)


@pytest_asyncio.fixture(scope="session")
async def prepare_database():
    """
    Drop all tables and recreate schema once per test session.  DESTRUCTIVE!! (but, wipe is currently disabled)
    """
    # TODO: We will not be wiping the DB here. -IF- we want to do this here, we will almost certainly need to seed
    #   our DB data unless we are doing this as part of tests that create their own data. We'll eventually have
    #   many of those so we might make two different kinds of fixtures: one for using the seed data that resets
    #   and re-seeds that data in a logical way for tests that use it and one that assumes the tests will create
    #   all of their own data, so it can do what is described here and just wipe and re-create the DB structure.
    async with test_engine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all)
        # await conn.run_sync(Base.metadata.create_all)
        pass


@pytest_asyncio.fixture
async def session() -> AsyncSession:
# async def session(prepare_database) -> AsyncSession:
    """
    Provides a new database session for each test.
    """
    async with TestAsyncSessionLocal() as session:
        yield session


# @pytest_asyncio.fixture(scope="function")
# async def session() -> AsyncSession:
#     async with TestAsyncSessionLocal() as session:
#         yield session


# WITH TRANSACTION ROLLBACK PER TEST: - BUT THIS STILL HAS OVERLAPPING SESSIONS WITH ASYNC - NO GOOD.
# @pytest_asyncio.fixture
# async def session(prepare_database) -> AsyncSession:
#     """
#     Provides a rollback-isolated database session for each test.
#     """
#     async with test_engine.connect() as conn:
#         trans = await conn.begin()
#         async_session = AsyncSession(bind=conn, expire_on_commit=False)
#         try:
#             yield async_session
#         finally:
#             await trans.rollback()
#             await async_session.close()


# TRYING TO GET SIMULTANEOUS ASYNC DB UNIT TESTS TO PLAY NICE WITH DB SESSIONS AND TRANSACTIONS.
# @pytest_asyncio.fixture
# async def session(prepare_database) -> AsyncSession:
#     """
#     Provides a rollback-safe, conflict-free session per test.
#     """
#     async with test_engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)
#
#     # create new connection and session per test
#     async with test_engine.connect() as conn:
#         # BEGIN outer transaction (so we can roll back everything in the end)
#         await conn.begin()
#         session = AsyncSession(bind=conn, expire_on_commit=False)
#
#         # begin a nested transaction for SAVEPOINT rollback
#         await session.begin_nested()
#
#         # handle SAVEPOINT restarts if test causes flush/commit
#         @event.listens_for(session.sync_session, "after_transaction_end")
#         def restart_savepoint(session_, transaction):
#             if transaction.nested and not transaction._parent.nested:
#                 session_.begin_nested()
#
#         try:
#             yield session
#         finally:
#             await session.rollback()
#             await session.close()
#             await conn.close()