from fastapi import APIRouter, Depends, status, Query
from app.schemas.rack import RackCreate, RackUpdate, RackResponse, RackListResponse
from app.services.rack_service import RackService
from app.utils.dependencies import get_rack_service

router = APIRouter(prefix="/racks", tags=["Racks"])

@router.get("/", response_model=RackListResponse)
async def list_racks(service: RackService = Depends(get_rack_service)):
    return await service.get_all()

@router.get("/{rack_id}", response_model=RackResponse)
async def get_rack(rack_id: int, service: RackService = Depends(get_rack_service)):
    return await service.get_by_id(rack_id)

@router.post("/", response_model=RackResponse, status_code=status.HTTP_201_CREATED)
async def create_rack(payload: RackCreate, serivce: RackService = Depends(get_rack_service)):
    return await serivce.create(payload)

@router.patch("/{rack_id}", response_model=RackResponse)
async def update_rack(rack_id: int, payload: RackUpdate, service: RackService = Depends(get_rack_service)):
    return await service.update(rack_id, payload)

@router.delete("/{rack_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_rack(rack_id: int, service: RackService = Depends(get_rack_service)):
    await service.delete(rack_id)
