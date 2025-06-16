import pytest


@pytest.mark.asyncio
async def test_AA_customers(async_http_client):
    response = await async_http_client.get("/customers/1")
    assert response.status_code == 200
    assert "Empresa Brasileira de Aeronáutica" in response.text or response.json()


@pytest.mark.asyncio
async def test_AB_customers(async_http_client):
    response = await async_http_client.get("/customers/13")
    assert response.status_code == 200
    assert "796 Dundas Street West" in response.text or response.json()


@pytest.mark.asyncio
async def test_AC_customers(async_http_client):
    response = await async_http_client.get("/customers/25")
    assert response.status_code == 200
    assert "Raj Bhavan Road" in response.text or response.json()

