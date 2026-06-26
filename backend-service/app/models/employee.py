from __future__ import annotations

import enum
from datetime import date
from typing import Optional

from sqlalchemy import Date, Enum as SAEnum, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, relationship, mapped_column

from .base import Base, TimestampMixin
from .user import User


class EmployeeStatus(str, enum.Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"


class EmploymentType(str, enum.Enum):
    PERMANENT = "PERMANENT"
    CONTRACT = "CONTRACT"
    SUBSTITUTE = "SUBSTITUTE"


class Employee(Base, TimestampMixin):
    __tablename__ = "employees"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    employee_code: Mapped[str] = mapped_column(String(20), unique=True, index=True, nullable=False)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False, unique=True, index=True)
    user: Mapped["User"] = relationship("User",back_populates="employee")

    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)

    gender: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)

    date_of_birth: Mapped[date] = mapped_column(Date, nullable=False)

    phone: Mapped[Optional[str]] = mapped_column(String(30), nullable=True)
    emergency_contact: Mapped[Optional[str]] = mapped_column(String(30), nullable=True)

    email: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

    department: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    designation: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)

    employment_type: Mapped[EmploymentType] = mapped_column(
        SAEnum(EmploymentType, name="employment_type_enum"), nullable=False
    )

    joining_date: Mapped[date] = mapped_column(Date, nullable=False)

    bank_account_number: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    ifsc_code: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)

    pan_number: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    aadhaar_number: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)

    status: Mapped[EmployeeStatus] = mapped_column(
        SAEnum(EmployeeStatus, name="employee_status_enum"), nullable=False, default=EmployeeStatus.ACTIVE
    )

    verification_status: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
