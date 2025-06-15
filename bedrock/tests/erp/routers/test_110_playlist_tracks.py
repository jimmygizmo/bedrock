import pytest


@pytest.mark.asyncio
async def test_AA_invoice_lines(async_http_client):
    response = await async_http_client.get("/invoice-lines/1")
    assert response.status_code == 200
    assert "MPEG audio file" in response.text or response.json()


@pytest.mark.asyncio
async def test_AB_invoice_lines(async_http_client):
    response = await async_http_client.get("/invoice-lines/3")
    assert response.status_code == 200
    assert "Protected MPEG-4 video file" in response.text or response.json()


@pytest.mark.asyncio
async def test_AC_invoice_lines(async_http_client):
    response = await async_http_client.get("/invoice-lines/5")
    assert response.status_code == 200
    assert "AAC audio file" in response.text or response.json()

