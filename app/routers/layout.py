from fastapi import APIRouter, Depends
from app.schemas.layout import LayoutRequest, LayoutResponse
from app.services.layout_service import LayoutService
from app.utils.dependencies import get_layout_service

router = APIRouter(prefix="/layout", tags=["layout"])

@router.post("/optimize", response_model=LayoutResponse)
async def optimize(payload: LayoutRequest, service: LayoutService = Depends(get_layout_service)):
    return await service.optimize(payload)