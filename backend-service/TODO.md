# TODO - Fix configuration consistency + PostgreSQL startup

## Step 1: Audit imports & inconsistent settings usage
- Identify any imports of `core.config` / `core.security` / `services.db` that should instead reference `app.core.*`.
- Fix by re-exporting the canonical `app.core.config.settings` from the duplicate modules, so any legacy imports still see identical Settings fields.

## Step 2: Unify config API (single source of truth)
- Update `backend-service/core/config.py` to import and re-export `settings` from `backend-service/app/core/config.py`.
- Update `backend-service/core/security.py` to re-export from `backend-service/app/core/security.py`.

## Step 3: Remove/avoid DB engine duplication side-effects
- Ensure `backend-service/services/db.py` never creates its own engine/session and does not import inconsistent settings.
- Make it re-export `engine`, `SessionLocal`, and `get_db` from `backend-service/app/services/db.py`.

## Step 4: Verify application startup with PostgreSQL
- Run backend startup.
- Confirm DB initialization (`create_all`) succeeds.
- If startup fails due to password auth, it must be fixed via `.env` (no hardcoded credentials).

## Step 5: Verify auth endpoints wiring
- Import/auth routes must use `app/services/db.py` and `app/core/config.py`.
- Confirm `GET /api/auth/me` works given a valid token.


