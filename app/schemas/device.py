from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class DeviceCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1, max_length=100)
    serial_number: str = Field(..., min_length=1, max_length=100)
    power_kw: float = Field(..., gt=0)
    rack_units: int = Field(..., ge=1, le=48)

class DeviceUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, min_length=1, max_length=100)
    power_kw: Optional[float] = Field(None, gt=0)
    rack_units: Optional[int] = Field(None, ge=1, le=48)

class DeviceResponse(BaseModel):
    id: int
    name: str
    description: str
    serial_number: str
    power_kw: float
    rack_units: int
    rack_id: Optional[int]
    rack_unit_postion: Optional[int]
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class DeviceListResponse(BaseModel):
    total: int
    items: list[DeviceResponse]

