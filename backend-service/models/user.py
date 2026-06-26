import enum
from sqlalchemy import String, Enum
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class UserRole(str, enum.Enum):
    ADMIN = "ADMIN"
    HR = "HR"
    STAFF = "STAFF"


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[UserRole] = mapped_column(Enum(UserRole), nullable=False, default=UserRole.STAFF)

    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, email={self.email!r}, role={self.role!r})"
