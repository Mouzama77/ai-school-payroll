from __future__ import annotations

from typing import Annotated, Callable

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from ..core.config import settings
from ..services.db import get_db

# Import user model + role enum that already exist in the project foundation.
from ..models.user import User, UserRole


security = HTTPBearer()


def _unauthorized() -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),   
    db: Session = Depends(get_db),
) -> User:
    token = credentials.credentials
    credentials_exception = _unauthorized()

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        sub = payload.get("sub")
        if sub is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user: User | None = db.query(User).filter(User.id == int(sub)).first()
    if user is None or not getattr(user, "is_active", True):
        raise credentials_exception
    return user


def require_role(*allowed_roles: UserRole) -> Callable[[User], User]:
    def _checker(user: User = Depends(get_current_user)) -> User:
        if user.role not in allowed_roles:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient role")
        return user

    return _checker

