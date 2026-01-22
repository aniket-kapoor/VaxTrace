from sqlalchemy.orm import Mapped , mapped_column
from ..core.database import Base
import uuid
from sqlalchemy.dialects.postgresql import UUID
from datetime import date , datetime 
from sqlalchemy import Date, String ,DateTime,Boolean, func, Float, Enum
from typing import Optional
import enum

from sqlalchemy import UniqueConstraint 
from sqlalchemy.orm  import relationship

from typing import TYPE_CHECKING   
if TYPE_CHECKING:
    from .patientDocs import PatientDocuments


class ApplicationStatus(str, enum.Enum):
    PROCESSING = "processing"
    APPROVED = "approved"
    REJECTED = "rejected"




class Patient(Base):
    __tablename__="patients"

    __table_args__ = (
        UniqueConstraint("parent_contact", "dob", "name", name="uq_patient_identity"),
    )

    id:Mapped[uuid.UUID]=mapped_column(UUID(as_uuid=True),
                                       primary_key=True,
                                       default=uuid.uuid4
                                       )
    name:Mapped[str]=mapped_column(String(16))
    gender:Mapped[str]
    dob: Mapped[date] = mapped_column(Date, nullable=False)
    father_name:Mapped[str]=mapped_column(String(16))


    parent_contact: Mapped[str] = mapped_column(
        String(16),
        nullable=False
    )
    state: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    district: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    city_or_village: Mapped[Optional[str]] = mapped_column(String(50))
    pincode: Mapped[Optional[str]] = mapped_column(String(10))
    Address:Mapped[str]=mapped_column(String(20), nullable=False)

    latitude: Mapped[Optional[float]] = mapped_column(Float)
    longitude: Mapped[Optional[float]] = mapped_column(Float)

   
    # Metadata
    
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    application_status:Mapped[ApplicationStatus]=mapped_column(
                                                 Enum(ApplicationStatus, native_enum=False), # native_enum=False uses VARCHAR in DB for easier migrations
                                                 default=ApplicationStatus.PROCESSING, 
                                                 nullable=False
                                             )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )

    

    documents: Mapped[list["PatientDocuments"]] = relationship(
            back_populates="patient",
        )

    


    




