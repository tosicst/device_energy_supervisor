from fastapi import HTTPException, status
from app.repositories.device_repo import DeviceRepository
from app.repositories.rack_repo import RackRepository
from app.schemas.device import DeviceResponse
from app.schemas.rack import RackResponse
from app.schemas.layout import LayoutRequest, LayoutResponse, RackLayoutDetail, DeviceData, RackData, LayoutResult


class LayoutService:
    def __init__(self, device_repo: DeviceRepository, rack_repo: RackRepository):
        self.device_repo = device_repo
        self.rack_repo = rack_repo

    async def optimize(self, request: LayoutRequest) -> LayoutResponse:
        devices = await self.device_repo.get_by_ids(request.device_ids)
        racks = await self.rack_repo.get_by_ids(request.rack_ids)

        if not devices:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No devices found")
        if not racks:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No racks found")
        
        device_map = {d.id: d for d in devices}
        rack_map = {r.id: r for r in racks}
        
        device_data = [
            DeviceData(id=d.id, name=d.name, power_kw=d.power_kw, rack_units=d.rack_units)
            for d in devices
        ]
        rack_data = [
            RackData(id=r.id, name=r.name, max_power_kw=r.max_power_kw, used_power_kw=0, total_units=r.total_units, used_units=0)
            for r in racks
        ]

        result = LayoutResult(layout={}, unplaced_devices={})
        
        devices_sorted = sorted(device_data, key=lambda d: d.power_kw, reverse=True)

        for device in devices_sorted:
            best_rack = None
            best_consumption = float("inf")
            
            for rack in rack_data:
                if rack.used_units + device.rack_units > rack.total_units:
                    continue

                if rack.used_power_kw + device.power_kw > rack.max_power_kw:
                    continue

                consumption = rack.used_power_kw + device.power_kw

                if consumption < best_consumption:
                    best_consumption = consumption
                    best_rack = rack

            if best_rack is None:
                result.unplaced_devices.append(device.id)
            
            if best_rack.id not in result.layout:
                result.layout[best_rack.id] = []
            result.layout[best_rack.id].append(device.id)
            best_rack.used_units += device.rack_units
            best_rack.used_power_kw += device.power_kw

        layout = []
        for rack_id, device_ids in result.layout.items():
            if rack_id not in rack_map:
                continue
            rack = rack_map[rack_id]
            assigned_devices = [device_map[did] for did in device_ids if did in device_map]
            total_power = sum(d.power_kw for d in assigned_devices)
            used_units = sum(d.rack_units for d in assigned_devices)

            layout.append(RackLayoutDetail(
                rack=RackResponse.model_validate(rack),
                devices=[DeviceResponse.model_validate(d) for d in assigned_devices],
                total_power_kw=round(total_power, 3),
                used_units=used_units,
                available_power_kw=round(rack.max_power_kw - total_power, 3),
                available_units=rack.total_units - used_units,
                utilization_percent=round((total_power / rack.max_power_kw) * 100, 1),
            ))

        unplaced = [
            DeviceResponse.model_validate(device_map[did])
            for did in result.unplaced_devices
            if did in device_map
        ]

        await self.save_layout(result.layout, device_map)

        return LayoutResponse(
            layout=layout,
            unplaced_devices=unplaced,
            total_devices=len(devices),
            placed_devices=len(devices) - len(unplaced),
            success=len(unplaced) == 0,
        )

    async def save_layout(self, layout: dict[int, list[int]], device_map: dict) -> None:
        for rack_id, device_ids in layout.items():
            position = 1
            for device_id in device_ids:
                if device_id in device_map:
                    device = device_map[device_id]
                    await self.device_repo.update_rack_assignment(device, rack_id, position)
                    position += device.rack_units

