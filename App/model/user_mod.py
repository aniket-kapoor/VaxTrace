from sqlalchemy import  Integer, String, Enum, Boolean
from sqlalchemy.orm import Mapped, mapped_column , relationship
import enum
from ..core.database import Base # Ensure this points to the new DeclarativeBase

from typing import TYPE_CHECKING   
if TYPE_CHECKING:
    from .vax_auditlog import VaccineAuditLog
    

class UserRole(str, enum.Enum):
    ADMIN = "admin"
    HEALTHWORKER = "worker"
    PARENT = "parent"

class Users(Base):
    __tablename__ = 'users'

    # Using the modern 2.0 style (Mapped) provides much better IDE autocomplete
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, nullable=True)
    email: Mapped[str] = mapped_column(String, index=True, unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)

    # Fixed: Added Column definition for is_active
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    # Improved Enum handling
    role: Mapped[UserRole] = mapped_column(
        Enum(UserRole, native_enum=False), # native_enum=False uses VARCHAR in DB for easier migrations
        default=UserRole.PARENT, 
        nullable=False
    )

    nin_id:Mapped[str]=mapped_column(String(10), nullable=True )
    institution_name:Mapped[str]=mapped_column(String(20), nullable=True)
    type_institution:Mapped[str]=mapped_column(String(20) , nullable=True)
    

    audit: Mapped[list["VaccineAuditLog"]] = relationship(
            back_populates="user",
            cascade="all, delete-orphan"
        )
    
    

