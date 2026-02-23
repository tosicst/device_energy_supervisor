from pydantic import BaseModel, Field
from app.schemas.device import DeviceResponse
from app.schemas.rack import RackResponse
from dataclasses import dataclass

class LayoutRequest(BaseModel):
    device_ids: list[int] = Field(..., min_length=1)
    rack_ids: list[int] = Field(..., min_length=1)

class RackLayoutDetail(BaseModel):
    rack: RackResponse
    devices: list[DeviceResponse]
    total_power_kw: float
    used_units: int
    available_power_kw: float
    available_units: int
    utilization_percent: float

class LayoutResponse(BaseModel):
    layout: list[RackLayoutDetail]
    unplaced_devices: list[DeviceResponse]
    total_devices: int
    placed_devices: int
    success: bool


@dataclass
class DeviceData:
    id: int
    name: str
    power_kw: float
    rack_units: int


@dataclass
class RackData:
    id: int
    name: str
    max_power_kw: float
    used_power_kw: float
    total_units: int
    used_units: int

@dataclass
class LayoutResult:
    layout: dict[int, list[int]]   # rack_id → [device_id, ...]
    unplaced_devices: list[int]
