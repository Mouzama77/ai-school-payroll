from __future__ import annotations
import enum

from sqlalchemy import Enum as SAEnum, String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import relationship

from .base import Base, TimestampMixin


class UserRole(str, enum.Enum):
    ADMIN = "ADMIN"
    HR = "HR"
    STAFF = "STAFF"


class User(Base, TimestampMixin):
    __tablename__ = "users"

    # NOTE: Existing auth dependency expects `sub` to be castable to `int`.
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    username: Mapped[str] = mapped_column(String(150), unique=True, index=True, nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)

    role: Mapped[UserRole] = mapped_column(
        SAEnum(UserRole),
        nullable=False,
        default=UserRole.STAFF,
    )
    
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    
    is_active: Mapped[bool] = mapped_column(nullable=False, default=True)
    employee: Mapped["Employee"] = relationship(
    "Employee",
    back_populates="user",
    uselist=False,
    cascade="all, delete-orphan"
    )
    def __repr__(self) -> str:
        return f"User(id={self.id!r}, email={self.email!r}, role={self.role!r})"
