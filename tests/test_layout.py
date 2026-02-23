import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy import text
from app.main import app
from app.database import engine

@pytest_asyncio.fixture
async def client():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac

@pytest_asyncio.fixture(autouse=True)
async def clean_db():
    async with engine.begin() as conn:
        await conn.execute(text("TRUNCATE TABLE devices, racks RESTART IDENTITY CASCADE"))

async def create_rack(client: AsyncClient, name: str, serial_number: str, description: str = "Some Rack", max_power_kw: float = 10.0, total_units: int = 42) -> dict:
    resp = await client.post("/api/v1/racks/", json={
        "name": name, "description": description, "serial_number": serial_number, "max_power_kw": max_power_kw, "total_units": total_units,
    })
    assert resp.status_code == 201
    return resp.json()

async def create_device(client: AsyncClient, name: str, serial_number: str, power_kw: float, rack_units: int = 1, description: str = "Some Device") -> dict:
    resp = await client.post("/api/v1/devices/", json={
        "name": name, "description": description, "serial_number": serial_number, "power_kw": power_kw, "rack_units": rack_units,
    })
    assert resp.status_code == 201
    return resp.json()

@pytest.mark.asyncio
async def test_optimize_layout_all_devices(client: AsyncClient):
    rack = await create_rack(client, name="Rack-001", serial_number="RC-001", max_power_kw=20)
    d1 = await create_device(client, name="D1", serial_number="DV-001", power_kw=2.0)
    d2 = await create_device(client, name="D2", serial_number="DV-002", power_kw=3.0)
    d3 = await create_device(client, name="D3", serial_number="DV-003", power_kw=0.5)

    resp = await client.post("/api/v1/layout/optimize", json={
        "device_ids": [d1["id"], d2["id"], d3["id"]],
        "rack_ids": [rack["id"]],
    })
    assert resp.status_code == 200

    data = resp.json()

    assert "layout" in data
    assert "unplaced_devices" in data
    assert "total_devices" in data
    assert "placed_devices" in data
    assert "success" in data

    assert data["success"] is True
    assert data["placed_devices"] == 3
    assert data["unplaced_devices"] == []