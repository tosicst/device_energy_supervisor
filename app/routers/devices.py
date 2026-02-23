from fastapi import APIRouter, Depends, status
from app.schemas.device import DeviceCreate, DeviceUpdate, DeviceResponse, DeviceListResponse
from app.services.device_service import DeviceService
from app.utils.dependencies import get_device_service

router = APIRouter(prefix="/devices", tags=["Devices"])

@router.get("/", response_model=DeviceListResponse)
async def list_devices(service: DeviceService = Depends(get_device_service)):
    return await service.get_all()

@router.get("/{device_id}", response_model=DeviceResponse)
async def get_device(device_id: int, service: DeviceService = Depends(get_device_service)):
    return await service.get_by_id(device_id)

@router.post("/", response_model=DeviceResponse, status_code=status.HTTP_201_CREATED)
async def create_device(payload: DeviceCreate, service: DeviceService = Depends(get_device_service)):
    return await service.create(payload)

@router.patch("/{device_id}", response_model=DeviceResponse)
async def update_device(device_id: int, payload: DeviceUpdate, service: DeviceService = Depends(get_device_service)):
    return await service.update(device_id, payload)

@router.delete("/{device_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_device(device_id: int, service: DeviceService = Depends(get_device_service)):
    await service.delete(device_id)
