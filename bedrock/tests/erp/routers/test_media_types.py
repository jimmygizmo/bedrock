import pytest


@pytest.mark.asyncio
async def test_AA_media_types(async_http_client):
    response = await async_http_client.get("/media-types/1")
    assert response.status_code == 200
    assert "MPEG audio file" in response.text or response.json()


@pytest.mark.asyncio
async def test_AB_media_types(async_http_client):
    response = await async_http_client.get("/media-types/3")
    assert response.status_code == 200
    assert "Protected MPEG-4 video file" in response.text or response.json()


@pytest.mark.asyncio
async def test_AC_media_types(async_http_client):
    response = await async_http_client.get("/media-types/5")
    assert response.status_code == 200
    assert "AAC audio file" in response.text or response.json()

