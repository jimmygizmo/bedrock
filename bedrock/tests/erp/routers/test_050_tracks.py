import pytest


@pytest.mark.asyncio
async def test_AA_tracks(async_http_client):
    response = await async_http_client.get("/tracks/1")
    assert response.status_code == 200
    assert "For Those About To Rock (We Salute You)" in response.text or response.json()


@pytest.mark.asyncio
async def test_AB_tracks(async_http_client):
    response = await async_http_client.get("/tracks/1747")
    assert response.status_code == 200
    assert "Lavender" in response.text or response.json()


@pytest.mark.asyncio
async def test_AC_tracks(async_http_client):
    response = await async_http_client.get("/tracks/3503")
    assert response.status_code == 200
    assert "Koyaanisqatsi" in response.text or response.json()

