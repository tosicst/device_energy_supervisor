import pytest
from unittest.mock import AsyncMock, MagicMock
from fastapi import HTTPException
from app.services.device_service import DeviceService
from app.services.rack_service import RackService
from app.schemas.device import DeviceCreate, DeviceUpdate
from app.schemas.rack import RackCreate, RackUpdate
from app.models.device import Device
from app.models.rack import Rack
from datetime import datetime

def make_device(**kwargs) -> Device:
    defaults = dict(
        id=1, name="Device-01", description="Some Device",
        serial_number="DV-001", power_kw=2.0, rack_units=2,
        rack_id=None, rack_unit_position=None,
        created_at=datetime.utcnow(), updated_at=datetime.utcnow(),
    )
    defaults.update(kwargs)
    device = MagicMock(spec=Device)
    for key, value in defaults.items():
        setattr(device, key, value)
    return device

def make_rack(**kwargs) -> Rack:
    defaults = dict(
        id=1, name="Rack-001", description="Some Rack",
        serial_number="RC-001", total_units=42, max_power_kw=10.0,
        created_at=datetime.utcnow(), updated_at=datetime.utcnow(),
        devices=[]
    )
    defaults.update(kwargs)
    rack = MagicMock(spec=Rack)
    for key, value in defaults.items():
        setattr(rack, key, value)
    return rack

# Device Service

class TestDeviceService:
    def setup_method(self):
        self.device_repo = MagicMock()
        self.rack_repo = MagicMock()
        self.service = DeviceService(self.device_repo, self.rack_repo)

    @pytest.mark.asyncio
    async def test_get_by_id_returns_device(self):
        self.device_repo.get_by_id = AsyncMock(return_value=make_device())
        result = await self.service.get_by_id(1)
        assert result.id == 1
        assert result.name == "Device-01"

    @pytest.mark.asyncio
    async def test_get_by_id_raises_404_when_not_found(self):
        self.device_repo.get_by_id = AsyncMock(return_value=None)
        with pytest.raises(HTTPException) as exc_info:
            await self.service.get_by_id(999)
        assert exc_info.value.status_code == 404

    @pytest.mark.asyncio
    async def test_create_raises_409_for_duplicate_serial(self):
        self.device_repo.get_by_serial = AsyncMock(return_value=make_device())
        payload = DeviceCreate(
            name="Device2", description="Some Device", serial_number="DV-001", power_kw=1.0, rack_units=1,
        )
        with pytest.raises(HTTPException) as exc_info:
            await self.service.create(payload)
        assert exc_info.value.status_code == 409

    @pytest.mark.asyncio
    async def test_create_succeeds_for_unique_serial(self):
        self.device_repo.get_by_serial = AsyncMock(return_value=None)
        self.device_repo.create = AsyncMock(return_value=make_device())
        payload = DeviceCreate(
            name="Device2", description="Some Device", serial_number="DV-002", power_kw=1.0, rack_units=1,
        )
        result = await self.service.create(payload)
        assert result.id == 1
        self.device_repo.create.assert_called_once()

    @pytest.mark.asyncio
    async def test_update_raises_404_when_not_found(self):
        self.device_repo.get_by_id = AsyncMock(return_value=None)
        with pytest.raises(HTTPException) as exc_info:
            await self.service.update(999, DeviceUpdate(description="Updated"))
        assert exc_info.value.status_code == 404

    @pytest.mark.asyncio
    async def test_update_calls_repo_update(self):
        existing = make_device()
        updated = make_device(description="Updated")
        self.device_repo.get_by_id = AsyncMock(return_value=existing)
        self.device_repo.update = AsyncMock(return_value=updated)
        result = await self.service.update(1, DeviceUpdate(description="Updated"))
        assert result.description == "Updated"
        self.device_repo.update.assert_called_once()

    @pytest.mark.asyncio
    async def test_delete_raises_404_when_not_found(self):
        self.device_repo.get_by_id = AsyncMock(return_value=None)
        with pytest.raises(HTTPException) as exc_info:
            await self.service.delete(999)
        assert exc_info.value.status_code == 404

    @pytest.mark.asyncio
    async def test_delete_calls_repo_delete(self):
        self.device_repo.get_by_id = AsyncMock(return_value=make_device)
        self.device_repo.delete = AsyncMock()
        await self.service.delete(1)
        self.device_repo.delete.assert_called_once()

# Rack Service

class TestRackService:
    def setup_method(self):
        self.rack_repo = MagicMock()
        self.service = RackService(self.rack_repo)

    @pytest.mark.asyncio
    async def test_get_by_id_return_rack(self):
        self.rack_repo.get_by_id = AsyncMock(return_value=make_rack())
        result = await self.service.get_by_id(1)
        assert result.id == 1
        assert result.name == "Rack-001"

    @pytest.mark.asyncio
    async def test_get_by_id_raises_404_when_not_found(self):
        self.rack_repo.get_by_id = AsyncMock(return_value=None)
        with pytest.raises(HTTPException) as exc_info:
            await self.service.get_by_id(999)
        assert exc_info.value.status_code == 404

    @pytest.mark.asyncio
    async def test_create_rack(self):
        self.rack_repo.create = AsyncMock(return_value=make_rack())
        result = await self.service.create(RackCreate(
            name="Rack-001", description="Some Rack", serial_number="RC-001", 
            max_power_kw=10.0, total_units = 42,
        ))
        assert result.name == "Rack-001"

    @pytest.mark.asyncio
    async def test_delete_succeeds_when_rack_empty(self):
        self.rack_repo.get_by_id = AsyncMock(return_value=make_rack(devices=[]))
        self.rack_repo.delete = AsyncMock()
        await self.service.delete(1)
        self.rack_repo.delete.assert_called_once()

    @pytest.mark.asyncio
    async def test_update_raises_404_when_not_found(self):
        self.rack_repo.get_by_id = AsyncMock(return_value=None)
        with pytest.raises(HTTPException) as exc_info:
            await self.service.update(999, RackUpdate(name="X"))
        assert exc_info.value.status_code == 404