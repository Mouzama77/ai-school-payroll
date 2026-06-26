"""Compatibility re-export.

Single source of truth for security helpers lives at:
`backend-service/app/core/security.py`.

Some legacy imports may reference `backend-service/core/security.py`.
Re-exporting prevents drift/inconsistent behavior.
"""

from app.core.security import *  # noqa: F403


