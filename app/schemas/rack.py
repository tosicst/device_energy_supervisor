from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class RackCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1, max_length=100)
    serial_number: str = Field(..., min_length=1, max_length=100)
    total_units: int = Field(default=42, ge=1, le=100)
    max_power_kw: float = Field(..., gt=0)

class RackUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = None
    total_units: Optional[int] = Field(None, ge=1, le=100)
    max_power_kw: Optional[float] = Field(None, gt=0)

class RackResponse(BaseModel):
    id: int
    name: str
    description: str
    total_units: int
    max_power_kw: float
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class RackListResponse(BaseModel):
    total: int
    items: list[RackResponse]

