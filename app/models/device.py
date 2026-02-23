from sqlalchemy import String, Float, Integer, DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base

class Device(Base):
    __tablename__ = "devices"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(String(100), nullable=True)
    serial_number: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)

    power_kw: Mapped[float] = mapped_column(Float, nullable=False)
    rack_units: Mapped[int] = mapped_column(Integer, default=1)

    rack_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("racks.id"), nullable=True)
    rack_unit_postion: Mapped[int | None] = mapped_column(Integer, nullable=True)

    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())

    rack: Mapped["Rack | None"] = relationship("Rack", back_populates="devices")


