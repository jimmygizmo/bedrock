import pytest


@pytest.mark.asyncio
async def test_AA_invoices(async_http_client):
    response = await async_http_client.get("/invoices/1")
    assert response.status_code == 200
    assert "Theodor-Heuss-Straße" in response.text or response.json()


@pytest.mark.asyncio
async def test_AB_invoices(async_http_client):
    response = await async_http_client.get("/invoices/206")
    assert response.status_code == 200
    assert "Lijnbaansgracht 120bg" in response.text or response.json()


@pytest.mark.asyncio
async def test_AC_invoices(async_http_client):
    response = await async_http_client.get("/invoices/412")
    assert response.status_code == 200
    assert "Community Centre" in response.text or response.json()

