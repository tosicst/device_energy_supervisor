from sqlalchemy import String, Float, Integer, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base

class Rack(Base):
    __tablename__ = "racks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(String(100), nullable=True)
    serial_number: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    total_units: Mapped[int] = mapped_column(Integer, default=42)
    max_power_kw: Mapped[float] = mapped_column(Float, nullable=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())

    devices: Mapped[list["Device"]] = relationship("Device", back_populates="rack")


