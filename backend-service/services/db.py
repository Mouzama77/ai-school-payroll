"""Compatibility re-export.

Canonical DB/session lives at `backend-service/app/services/db.py`.

Some legacy imports may reference `backend-service/services/db.py`.
Re-exporting prevents mismatched settings/engine creation.
"""

from app.services.db import SessionLocal, engine, get_db  # noqa: F401



