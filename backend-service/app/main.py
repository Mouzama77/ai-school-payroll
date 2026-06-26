from fastapi import FastAPI

from app.api.routes.health import router as health_router
from app.api.routes.auth import router as auth_router
from app.models.base import Base as AppBase
from app.models.user import User
from app.models.employee import Employee
from app.services.db import engine


def create_app() -> FastAPI:
    app = FastAPI()

    @app.on_event("startup")
    def _startup() -> None:
        # Foundation automatic DB initialization.
        # Uses the SQLAlchemy Base that future business models will extend.
        AppBase.metadata.create_all(bind=engine)

    app.include_router(health_router, prefix="/api")
    app.include_router(auth_router, prefix="/api")
    return app


app = create_app()



