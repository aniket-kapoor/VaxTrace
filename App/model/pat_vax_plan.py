from ..core.database import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer,String, Boolean , DateTime , func , Date,UniqueConstraint, ForeignKey
import uuid
from sqlalchemy.dialects.postgresql import UUID


class PatientVaccinePlan(Base):
    __tablename__ = "patient_vaccine_plan"

    __table_args__ = (
        UniqueConstraint(
            "patient_id", "vaccine_id", "dose_number",
            name="uq_patient_vaccine_plan"
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

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

    dose_number: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    due_date: Mapped[Date] = mapped_column(
        Date,
        nullable=False
    )

    status: Mapped[str] = mapped_column(
        String(20),
        default="PENDING"  # PENDING, COMPLETED, MISSED
    )

    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    verified_by_worker: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=False
    )
    
    verified_at: Mapped[DateTime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )