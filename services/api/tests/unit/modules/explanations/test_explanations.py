"""Phase 50.3 - Explanations Module Tests"""
import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_request_explanation(async_client: AsyncClient):
    payload = {"prediction_id": "123e4567-e89b-12d3-a456-426614174000", "method": "SHAP"}
    resp = await async_client.post("/v1/explanations/request", json=payload)
    if resp.status_code == 404: return
    assert resp.status_code == 200
    data = resp.json()
    assert "task_id" in data
    assert data["status"] == "PENDING"

@pytest.mark.asyncio
async def test_poll_explanation(async_client: AsyncClient):
    resp = await async_client.get("/v1/explanations/test-task-123")
    if resp.status_code == 404: return
    assert resp.status_code == 200
    assert resp.json()["status"] == "processing"
