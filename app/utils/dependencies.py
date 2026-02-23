from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.repositories.rack_repo import RackRepository
from app.repositories.device_repo import DeviceRepository
from app.services.rack_service import RackService
from app.services.device_service import DeviceService
from app.services.layout_service import LayoutService
import logging

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

# Repositories

def get_rack_repo(db: AsyncSession = Depends(get_db)) -> RackRepository:
    bind = db.get_bind()
    print(str(bind.url))
    return RackRepository(db)

def get_device_repo(db: AsyncSession = Depends(get_db)) -> DeviceRepository:
    return DeviceRepository(db)

# Services

def get_rack_service(repo: RackRepository = Depends(get_rack_repo)) -> RackService:
    return RackService(repo)

def get_device_service(device_repo: DeviceRepository = Depends(get_device_repo), rack_repo: RackRepository = Depends(get_rack_repo)) -> DeviceService:
    return DeviceService(device_repo, rack_repo)

def get_layout_service(device_repo: DeviceRepository = Depends(get_device_repo), rack_repo: RackRepository = Depends(get_rack_repo)) -> LayoutService:
    return LayoutService(device_repo, rack_repo)

