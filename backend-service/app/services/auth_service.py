"""Compatibility re-export.

Canonical auth service lives at `backend-service/services/auth_service.py`.

The auth router imports from `app.services.auth_service`, so this module keeps
imports stable without duplicating business logic.
"""

from services.auth_service import authenticate_user, register_user  # noqa: F401
