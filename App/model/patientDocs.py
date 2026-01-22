from sqlalchemy.orm import Mapped , mapped_column 
from ..core.database import Base
import uuid
from sqlalchemy.dialects.postgresql import UUID
from datetime import date , datetime 
from sqlalchemy import Date, String ,DateTime,Boolean, func, Float,ForeignKey
from sqlalchemy.orm import relationship
from typing import Optional

from typing import TYPE_CHECKING   
if TYPE_CHECKING:
    from .patient_mod import Patient


class PatientDocuments(Base):
    __tablename__="patient_documents"

    id :Mapped[uuid.UUID]=mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,   # 🔥 THIS WAS MISSING
        nullable=False
    )

    patient_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("patients.id"),
        nullable=False
    )

    document_type:Mapped[str] = mapped_column(String(50), nullable=False)
    file_path:Mapped[str]= mapped_column(String(255), nullable=False)

  

    patient: Mapped[list["Patient"]] = relationship(
            back_populates="documents",
        )
    





