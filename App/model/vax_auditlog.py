from sqlalchemy.orm import Mapped , mapped_column , relationship
from ..core.database import Base

import uuid
from sqlalchemy.dialects.postgresql import UUID
from datetime import date , datetime 
from sqlalchemy import Date, String ,DateTime,Boolean, func, Float, Integer,String,ForeignKey

from typing import Optional

from typing import TYPE_CHECKING   
if TYPE_CHECKING:
    from .user_mod import Users
    from .pat_vax_plan import PatientVaccinePlan



class VaccineAuditLog(Base):
    __tablename__ = "vaccine_audit_logs"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    plan_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("patient_vaccine_plan.id"),
        nullable=False
    )

    old_status: Mapped[str] = mapped_column(
        String(20),
        nullable=False
    )

    new_status: Mapped[str] = mapped_column(
        String(20),
        nullable=False
    )

    changed_by: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id"),
        nullable=True
        
    )

    changed_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=True
    )

    user: Mapped["Users"] = relationship(
    back_populates="audit"
    )

    
    # VaccineAuditLog
    plan: Mapped["PatientVaccinePlan"] = relationship(
    back_populates="audit"
    )







