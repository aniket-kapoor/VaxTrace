from ..core.database import Base
from sqlalchemy.orm import Mapped, mapped_column , relationship 
from sqlalchemy import Integer,String, Boolean , DateTime , func , ForeignKey
import uuid
from sqlalchemy.dialects.postgresql import UUID

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .vax_master import Vaccine


class VaccineScheduleMaster(Base):
    __tablename__ = "vaccine_schedule"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
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

    min_age_days: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    max_age_days: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True
    )

    is_booster: Mapped[bool] = mapped_column(
        Boolean,
        default=False
    )

    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    vaccine: Mapped["Vaccine"] = relationship(
        back_populates="schedules"
    )
