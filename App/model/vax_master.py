from ..core.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer,String, Boolean , DateTime , func
import uuid
from sqlalchemy.dialects.postgresql import UUID

from typing import TYPE_CHECKING    # to resolve the string wari=nings in relationships due to overprotectecive
                                    #nature of pylance
if TYPE_CHECKING:
    from .vax_schedule import VaccineScheduleMaster



class Vaccine(Base):

    __tablename__="vaccine_master"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    vaccine_code: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False
    )

    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    schedules: Mapped[list["VaccineScheduleMaster"]] = relationship(
        back_populates="vaccine",
        cascade="all, delete-orphan"
    )
    
    
