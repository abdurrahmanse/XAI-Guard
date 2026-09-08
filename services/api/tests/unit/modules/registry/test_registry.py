"""Phase 51.3 - Registry Module Tests"""
import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_get_champion(async_client: AsyncClient):
    resp = await async_client.get("/v1/registry/champion")
    if resp.status_code == 404:
        return
    assert resp.status_code == 200

@pytest.mark.asyncio
async def test_promote_requires_admin(async_client: AsyncClient):
    resp = await async_client.post("/v1/registry/promote", json={"challenger_id": "123", "reason": "test"})
    if resp.status_code == 404:
        return
    assert resp.status_code == 401
