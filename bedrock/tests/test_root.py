import pytest


@pytest.mark.asyncio
async def test_root(async_http_client):
    response = await async_http_client.get("/")
    assert response.status_code == 200
    assert "This is the root" in response.text or response.json()

