import pytest


@pytest.mark.asyncio
async def test_AA_genres(async_http_client):
    response = await async_http_client.get("/genres/1")
    assert response.status_code == 200
    assert "Rock" in response.text or response.json()


@pytest.mark.asyncio
async def test_AB_genres(async_http_client):
    response = await async_http_client.get("/genres/13")
    assert response.status_code == 200
    assert "Heavy Metal" in response.text or response.json()


@pytest.mark.asyncio
async def test_AC_genres(async_http_client):
    response = await async_http_client.get("/genres/25")
    assert response.status_code == 200
    assert "Opera" in response.text or response.json()

