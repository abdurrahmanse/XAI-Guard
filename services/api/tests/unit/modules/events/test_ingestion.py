"""Unit tests for security event ingestion — protocol enums and field validation."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../../../.."))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../../../../app"))
"""
services/api/tests/unit/modules/events/test_ingestion.py
========================================================
Test suite for event ingestion, deduplication, storage, and queuing.
"""
from __future__ import annotations

from app.modules.events.models import ProtocolEnum, DatasetSourceEnum
import pytest
from httpx import AsyncClient
from redis.asyncio.client import Redis
from sqlalchemy.ext.asyncio import AsyncSession

# Use the app initialized in conftest.py or main depending on your test setup.
# Here we assume a test fixture `async_client` provides an HTTPX client
# hitting the FastAPI app, and `redis_client` provides a test Redis instance.

def test_protocol_enum_covers_common_protocols():
    values = {p.value for p in ProtocolEnum}
    assert "TCP" in values
    assert "UDP" in values
    assert "ICMP" in values
    assert "OTHER" in values  # catch-all for unknown protocols
@pytest.mark.asyncio
async def test_ingest_valid_batch(async_client: AsyncClient, redis_client: Redis):
    """Test 1: valid batch of events returns accepted_count."""
    # Ensure stream is clean
    await redis_client.delete("events:pending")
    
    payload = {
        "events": [
            {
                "timestamp": 1690000000.0,
                "source_ip": "192.168.1.100",
                "destination_ip": "10.0.0.1",
                "source_port": 12345,
                "destination_port": 80,
                "protocol": "TCP",
                "bytes_in": 500,
                "bytes_out": 1500,
                "duration_ms": 100,
                "features": {"f1": 0.5, "f2": 1.5}
            }
        ]
    }
    
    response = await async_client.post("/v1/events/ingest", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["accepted_count"] == 1
    assert data["duplicate_count"] == 0
    assert len(data["accepted_event_ids"]) == 1

@pytest.mark.asyncio
async def test_ingest_duplicates(async_client: AsyncClient, redis_client: Redis):
    """Test 2: batch with duplicates returns duplicate_count."""
    payload = {
        "events": [
            {
                "timestamp": 1690000001.0,
                "source_ip": "192.168.1.101",
                "destination_ip": "10.0.0.2",
                "source_port": 12345,
                "destination_port": 80,
                "protocol": "TCP",
                "bytes_in": 500,
                "bytes_out": 1500,
                "duration_ms": 100,
            }
        ]
    }
    
    # First request: should be accepted
    res1 = await async_client.post("/v1/events/ingest", json=payload)
    assert res1.status_code == 200
    assert res1.json()["accepted_count"] == 1
    assert res1.json()["duplicate_count"] == 0
    
    # Second request: exactly identical event, should be flagged duplicate
    res2 = await async_client.post("/v1/events/ingest", json=payload)
    assert res2.status_code == 200
    assert res2.json()["accepted_count"] == 0
    assert res2.json()["duplicate_count"] == 1

def test_dataset_source_covers_all_four_benchmarks():
    """All four research datasets must be represented."""
    values = {d.value for d in DatasetSourceEnum}
    assert "NSL_KDD" in values
    assert "CICIDS_2017" in values
    assert "UNSW_NB15" in values
    assert "BETH" in values
@pytest.mark.asyncio
async def test_ingest_max_limit(async_client: AsyncClient):
    """Test 3: batch exceeding max limit returns 422."""
    payload = {
        "events": [
            {
                "timestamp": 1690000000.0,
                "source_ip": "1.1.1.1",
                "destination_ip": "2.2.2.2",
                "source_port": 1,
                "destination_port": 2,
                "protocol": "TCP",
                "bytes_in": 1,
                "bytes_out": 1,
                "duration_ms": 1,
            } for _ in range(1001)
        ]
    }
    response = await async_client.post("/v1/events/ingest", json=payload)
    assert response.status_code == 422
    assert "events" in response.text
    assert "at most 1000 items" in response.text.lower() or "too_long" in response.text.lower()


def test_dataset_source_includes_live():
    """Production live traffic must be a valid source."""
    assert "LIVE" in {d.value for d in DatasetSourceEnum}


def test_protocol_enum_values_are_uppercase():
    for p in ProtocolEnum:
        assert p.value == p.value.upper()


def test_security_event_required_fields():
    from app.modules.events.models import SecurityEvent
    # SQLAlchemy uses __mapper__.columns for the real field list
    column_names = {c.key for c in SecurityEvent.__mapper__.columns}
    required = ["source_ip", "destination_ip", "source_port",
                "destination_port", "protocol", "features", "dataset_source"]
    for field in required:
        assert field in column_names, f"SecurityEvent missing: {field}"
@pytest.mark.asyncio
async def test_ingest_invalid_format(async_client: AsyncClient):
    """Test 4: invalid field types return 422 with details."""
    payload = {
        "events": [
            {
                "timestamp": "not-a-number",
                "source_ip": "1.1.1.1",
                "destination_ip": "2.2.2.2",
                "source_port": 1,
                "destination_port": 2,
                "protocol": "INVALID",
                "bytes_in": 1,
                "bytes_out": 1,
                "duration_ms": 1,
            }
        ]
    }
    response = await async_client.post("/v1/events/ingest", json=payload)
    assert response.status_code == 422
    
@pytest.mark.asyncio
async def test_empty_batch(async_client: AsyncClient):
    """Test 6: empty batch returns 422."""
    payload = {"events": []}
    response = await async_client.post("/v1/events/ingest", json=payload)
    assert response.status_code == 422
    
@pytest.mark.asyncio
async def test_redis_stream_population(async_client: AsyncClient, redis_client: Redis):
    """Test 7: Redis Stream contains exactly accepted_count new entries."""
    # Ensure stream is clean
    await redis_client.delete("events:pending")
    
    payload = {
        "events": [
            {
                "timestamp": 1690000003.0,
                "source_ip": "192.168.1.103",
                "destination_ip": "10.0.0.4",
                "source_port": 12345,
                "destination_port": 80,
                "protocol": "TCP",
                "bytes_in": 500,
                "bytes_out": 1500,
                "duration_ms": 100,
            }
        ]
    }
    
    res = await async_client.post("/v1/events/ingest", json=payload)
    assert res.status_code == 200
    assert res.json()["accepted_count"] == 1
    
    # Verify stream length
    stream_len = await redis_client.xlen("events:pending")
    assert stream_len == 1
