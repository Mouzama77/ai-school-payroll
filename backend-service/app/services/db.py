from __future__ import annotations

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from ..core.config import settings


# SQLAlchemy Engine + Session
# PostgreSQL support via DATABASE_URL (expects postgresql+psycopg or postgresql+psycopg[binary])
connect_args: dict[str, object] = {}

# SQLite needs check_same_thread=False for FastAPI
if settings.DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

# For SQLite, omit pool_size/max_overflow to avoid None arithmetic inside SQLAlchemy.
if settings.DATABASE_URL.startswith("sqlite"):
    engine = create_engine(
        settings.DATABASE_URL,
        pool_pre_ping=True,
        connect_args=connect_args,
    )
else:
    engine = create_engine(
        settings.DATABASE_URL,
        pool_pre_ping=True,
        pool_size=10,
        max_overflow=20,
        connect_args=connect_args,
    )


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Base metadata (for startup create_all)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

