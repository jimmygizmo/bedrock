import pytest


@pytest.mark.asyncio
async def test_AA_albums(async_http_client):
    response = await async_http_client.get("/albums/1")
    assert response.status_code == 200
    assert "For Those About To Rock We Salute You" in response.text or response.json()


@pytest.mark.asyncio
async def test_AB_albums(async_http_client):
    response = await async_http_client.get("/albums/173")
    assert response.status_code == 200
    assert "No More Tears (Remastered)" in response.text or response.json()


@pytest.mark.asyncio
async def test_AC_albums(async_http_client):
    response = await async_http_client.get("/albums/347")
    assert response.status_code == 200
    assert "Koyaanisqatsi (Soundtrack from the Motion Picture)" in response.text or response.json()

