from fastapi import HTTPException, status
from app.repositories.device_repo import DeviceRepository
from app.repositories.rack_repo import RackRepository
from app.schemas.device import DeviceCreate, DeviceUpdate, DeviceResponse, DeviceListResponse

class DeviceService:
    """
    """

    def __init__(self, device_repo: DeviceRepository, rack_repo: RackRepository):
        self.device_repo = device_repo
        self.rack_repo = rack_repo

    async def get_all(self) -> DeviceListResponse:
        total, devices = await self.device_repo.get_all()
        return DeviceListResponse(total=total, items=[DeviceResponse.model_validate(d) for d in devices])

    async def get_by_id(self, device_id: int) -> DeviceResponse:
        device = await self.device_repo.get_by_id(device_id)
        if not device:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Device not found")
        return DeviceResponse.model_validate(device)
    
    async def create(self, data: DeviceCreate) -> DeviceResponse:
        existing = await self.device_repo.get_by_serial(data.serial_number)
        if existing:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Device with serial number '{data.serial_number}' aleady exists")
        device = await self.device_repo.create(data)
        return DeviceResponse.model_validate(device)
    
    async def update(self, device_id: int, data: DeviceUpdate) -> DeviceResponse:
        device = await self.device_repo.get_by_id(device_id)
        if not device:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Device not found")
        updated = await self.device_repo.update(device, data)
        return DeviceResponse.model_validate(updated)
    
    async def delete(self, device_id: int) -> None:
        device = await self.device_repo.get_by_id(device_id)
        if not device:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Device not found")
        await self.device_repo.delete(device)