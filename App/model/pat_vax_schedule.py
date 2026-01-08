from sqlalchemy.orm import Mapped , mapped_column
from ..core.database import Base

import uuid
from sqlalchemy.dialects.postgresql import UUID
from datetime import date , datetime 
from sqlalchemy import Date, String ,DateTime,Boolean, func, Float, Integer,String,ForeignKey

from typing import Optional



class VaxinRecord(Base):
    __tablename__ = 'vaccination'

    id:Mapped[int]=mapped_column(Integer,primary_key=True,index=True)

    patient_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("patients.id"),
        nullable=False
    )
    vaccine_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("vaccine_master.id"),
        nullable=False
    )
    dose_no: Mapped[int] = mapped_column(ForeignKey("vaccine_schedule.id"), nullable=False)

    vaccination_date: Mapped[Date | None] = mapped_column(Date,nullable=True)

    recorded_date: Mapped[Date] = mapped_column(Date,server_default=func.current_date())

    vaccination_status: Mapped[str] = mapped_column(
        String(30),
        nullable=False
    )

    data_source: Mapped[str | None] = mapped_column(
        String(30),
        nullable=True
    )

    ocr_confidence: Mapped[float | None] = mapped_column(
        nullable=True
    )

    verified_by: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        nullable=True
    )

    verified_at: Mapped[DateTime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )








