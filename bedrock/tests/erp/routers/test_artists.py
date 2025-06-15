import pytest


@pytest.mark.asyncio
async def test_AA_artists(async_http_client):
    response = await async_http_client.get("/artists/1")
    assert response.status_code == 200
    assert "AC/DC" in response.text or response.json()


@pytest.mark.asyncio
async def test_AB_artists(async_http_client):
    response = await async_http_client.get("/artists/134")
    assert response.status_code == 200
    assert "Stone Temple Pilots" in response.text or response.json()


@pytest.mark.asyncio
async def test_AC_artists(async_http_client):
    response = await async_http_client.get("/artists/275")
    assert response.status_code == 200
    assert "Philip Glass Ensemble" in response.text or response.json()

