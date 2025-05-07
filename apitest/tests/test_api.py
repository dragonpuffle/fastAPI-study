import pytest
from httpx import ASGITransport, AsyncClient

from apitest.main import app


@pytest.mark.asyncio
async def test_get_books():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/books")
        data = response.json()
        assert response.status_code == 200
        assert len(data) == 2


@pytest.mark.asyncio
async def test_post_books():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post(
            "/books",
            json={
                "title": "vse o minecraft",
                "author": "andrew",
            },
        )
        data = response.json()
        assert response.status_code == 200
        assert data == {"ok": True}
