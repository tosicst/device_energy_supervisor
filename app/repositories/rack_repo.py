from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.models.rack import Rack
from app.schemas.rack import RackCreate, RackUpdate

class RackRepository:
    """
    """

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self) -> tuple[int, list[Rack]]:
        total = await self.db.scalar(select(func.count()).select_from(Rack))
        result = await self.db.execute(select(Rack))
        return total, result.scalars().all()

    async def get_by_id(self, rack_id: int) -> Rack | None:
        result = await self.db.execute(select(Rack).where(Rack.id == rack_id))
        return result.scalar_one_or_none()
    
    async def get_by_ids(self, rack_ids: list[int]) -> list[Rack]:
        result = await self.db.execute(select(Rack).where(Rack.id.in_(rack_ids)))
        return result.scalars().all()
    
    async def create(self, data: RackCreate) -> Rack:
        rack = Rack(**data.model_dump())
        self.db.add(rack)
        await self.db.flush()
        await self.db.refresh(rack)
        return rack
    
    async def update(self, rack: Rack, data: RackUpdate) -> Rack:
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(rack, field, value)
        await self.db.flush()
        await self.db.refresh(rack)
        return rack
    
    async def delete(self, rack: Rack) -> None:
        await self.db.delete(rack)
        await self.db.flush()