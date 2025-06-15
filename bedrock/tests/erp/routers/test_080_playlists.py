import pytest


@pytest.mark.asyncio
async def test_AA_playlists(async_http_client):
    response = await async_http_client.get("/playlists/1")
    assert response.status_code == 200
    assert "Music" in response.text or response.json()


@pytest.mark.asyncio
async def test_AB_playlists(async_http_client):
    response = await async_http_client.get("/playlists/9")
    assert response.status_code == 200
    assert "Music Videos" in response.text or response.json()


@pytest.mark.asyncio
async def test_AC_playlists(async_http_client):
    response = await async_http_client.get("/playlists/18")
    assert response.status_code == 200
    assert "On-The-Go 1" in response.text or response.json()

