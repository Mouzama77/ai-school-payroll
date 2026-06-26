from sqlalchemy.orm import Session

from app.core.security import create_access_token, hash_password, verify_password
from app.models.user import User, UserRole


def register_user(
    db: Session,
    *,
    username: str,
    email: str,
    full_name: str,
    password: str,
    role: UserRole = UserRole.STAFF,
) -> User:
    existing = db.query(User).filter(User.email == email).first()
    if existing is not None:
        raise ValueError("Email already registered")
    existing = db.query(User).filter(User.username == username).first()
    if existing is not None:
        raise ValueError("Username already exists")

    user = User(
        username=username,
        email=email,
        full_name=full_name,
        role=role,
        password_hash=hash_password(password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def authenticate_user(db: Session, *, email: str, password: str) -> str:
    user: User | None = db.query(User).filter(User.email == email).first()
    if user is None:
        raise ValueError("Invalid credentials")

    if not verify_password(password, user.password_hash):
        raise ValueError("Invalid credentials")

    token = create_access_token(subject=str(user.id), role=user.role.value)
    return token
