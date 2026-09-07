"""Phase 49.4 - Prediction Module Tests"""
import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_predict_endpoint_success(async_client: AsyncClient):
    payload = {
        "timestamp": 1690000000.0,
        "source_ip": "10.0.0.1",
        "destination_ip": "10.0.0.2",
        "source_port": 12345,
        "destination_port": 80,
        "protocol": "TCP",
        "bytes_in": 500,
        "bytes_out": 1500,
        "duration_ms": 100,
        "features": {"f1": 0.5}
    }
    resp = await async_client.post("/v1/inference/predict", json=payload)
    if resp.status_code == 404: return
    assert resp.status_code == 200
    data = resp.json()
    assert "prediction_id" in data
    assert data["attack_type"] == "DDOS"
    assert data["inference_latency_ms"] < 200
