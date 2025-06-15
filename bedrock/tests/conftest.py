import pytest_asyncio
from httpx import AsyncClient


@pytest_asyncio.fixture
async def async_http_client():
    """Real network client to running FastAPI service on port 48000."""
    async with AsyncClient(base_url="http://localhost:48000") as client:
        yield client

