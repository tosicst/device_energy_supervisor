from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.database import engine, Base
from app.routers import devices, racks, layout

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()

app = FastAPI(lifespan=lifespan)

PREFIX = "/api/v1"
app.include_router(racks.router, prefix=PREFIX)
app.include_router(devices.router, prefix=PREFIX)
app.include_router(layout.router, prefix=PREFIX)

@app.get("/health", tags=["Health"])
async def health():
    return {"status": "ok"}