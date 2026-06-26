from typing import Literal

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session

from ..deps import get_current_user
from ...models.user import UserRole
from ...services.auth_service import authenticate_user, register_user
from ...services.db import get_db

router = APIRouter(prefix="/auth", tags=["auth"])


class RegisterRequest(BaseModel):
    username: str
    email: EmailStr
    full_name: str
    password: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: Literal["bearer"] = "bearer"


@router.post("/register", response_model=dict)
def register(payload: RegisterRequest, db: Session = Depends(get_db)) -> dict:
    try:
        user = register_user(
            db,
            username=payload.username,
            email=payload.email,
            full_name=payload.full_name,
            password=payload.password,
            role=UserRole.STAFF,
        )
        return {"id": user.id, "email": user.email, "role": user.role.value, "full_name": user.full_name}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)) -> TokenResponse:
    try:
        token = authenticate_user(db, email=payload.email, password=payload.password)
        return TokenResponse(access_token=token)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))


# Example protected endpoint hook (no payroll logic yet)
@router.get("/me")
def me(user=Depends(get_current_user)) -> dict:
    return {"id": user.id, "email": user.email, "role": user.role.value, "full_name": user.full_name}
