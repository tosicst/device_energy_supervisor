from fastapi import HTTPException, status
from app.repositories.rack_repo import RackRepository
from app.schemas.rack import RackCreate, RackUpdate, RackResponse, RackListResponse

class RackService:
    """
    """

    def __init__(self, repo: RackRepository):
        self.repo = repo

    async def get_all(self) -> RackListResponse:
        total, racks = await self.repo.get_all()
        return RackListResponse(total=total, items=[RackResponse.model_validate(r) for r in racks])

    async def get_by_id(self, rack_id: int) -> RackResponse:
        rack = await self.repo.get_by_id(rack_id)
        if not rack:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Rack not found")
        return RackResponse.model_validate(rack)

    async def create(self, data: RackCreate) -> RackResponse:
        rack = await self.repo.create(data)
        return RackResponse.model_validate(rack)

    async def update(self, rack_id: int, data: RackUpdate) -> RackResponse:
        rack = await self.repo.get_by_id(rack_id)
        if not rack:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Rack not found")
        update = await self.repo.update(rack, data)
        return RackResponse.model_validate(update)

    async def delete(self, rack_id: int) -> None:
        rack = await self.repo.get_by_id(rack_id)
        if not rack:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Rack not found")
        await self.repo.delete(rack)
