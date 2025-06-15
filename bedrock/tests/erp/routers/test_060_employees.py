import pytest


@pytest.mark.asyncio
async def test_AA_employees(async_http_client):
    response = await async_http_client.get("/employees/1")
    assert response.status_code == 200
    assert "Adams" in response.text or response.json()


@pytest.mark.asyncio
async def test_AB_employees(async_http_client):
    response = await async_http_client.get("/employees/5")
    assert response.status_code == 200
    assert "Johnson" in response.text or response.json()


@pytest.mark.asyncio
async def test_AC_employees(async_http_client):
    response = await async_http_client.get("/employees/8")
    assert response.status_code == 200
    assert "Callahan" in response.text or response.json()

