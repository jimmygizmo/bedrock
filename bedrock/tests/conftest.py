import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from magma.main import app
from magma.core.database import Base, async_engine
from magma.core.dependencies import get_db_async_session


@pytest.fixture(scope="session", autouse=True)
async def setup_test_db():
    """Create and drop tables around the entire test session."""
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@pytest.fixture
async def session() -> AsyncSession:
    """Yield a new database session per test."""
    async with get_db_async_session() as s:
        yield s


@pytest.fixture
async def client() -> AsyncClient:
    """Provide a FastAPI test client using httpx."""
    async with AsyncClient(app=app, base_url="http://localhost:48000") as c:
        yield c

