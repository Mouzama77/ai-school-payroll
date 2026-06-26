"""Compatibility re-export.

This project intentionally has a single source of truth for configuration at:
`backend-service/app/core/config.py`.

Some legacy imports may still reference `backend-service/core/config.py`.
Re-exporting `settings` keeps configuration consistent and prevents mismatched
field names (e.g., lowercase vs uppercase) across modules.
"""

from app.core.config import settings  # noqa: F401


