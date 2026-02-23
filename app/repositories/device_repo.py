from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.models.device import Device
from app.schemas.device import DeviceCreate, DeviceUpdate

class DeviceRepository:
    """
    """

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self) -> tuple[int, list[Device]]:
        total = await self.db.scalar(select(func.count()).select_from(Device))
        result = await self.db.execute(select(Device))
        return total, result.scalars().all()

    async def get_by_id(self, device_id: int) -> Device | None:
        result = await self.db.execute(select(Device).where(Device.id == device_id))
        return result.scalar_one_or_none()
    
    async def get_by_ids(self, device_ids: list[int]) -> list[Device]:
        result = await self.db.execute(select(Device).where(Device.id.in_(device_ids)))
        return result.scalars().all()
    
    async def get_by_serial(self, serial_number: str) -> Device | None:
        result = await self.db.execute(select(Device).where(Device.serial_number == serial_number))
        return result.scalar_one_or_none()
    
    async def create(self, data: DeviceCreate) -> Device:
        device = Device(**data.model_dump())
        self.db.add(device)
        await self.db.flush()
        await self.db.refresh(device)
        return device
    
    async def update(self, device: Device, data: DeviceUpdate) -> Device:
        for field, vlaue in data.model_dump(exclude_unset=True).items():
            setattr(device, field, vlaue)
        await self.db.flush()
        await self.db.refresh(device)
        return device
    
    async def update_rack_assignment(self, device: Device, rack_id: int | None, postion: int | None) -> Device:
        device.rack_id = rack_id
        device.rack_unit_postion = postion
        await self.db.flush()
        await self.db.refresh(device)
        return device
    
    async def delete(self, device: Device) -> None:
        await self.db.delete(device)
        await self.db.flush()
