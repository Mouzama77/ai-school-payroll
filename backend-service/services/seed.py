from sqlalchemy.orm import Session

from ..models.user import User, UserRole
from .auth_service import register_user


def seed_default_roles_and_admin(db: Session) -> None:
    """
    Foundation seed:
    - Ensure at least one ADMIN user exists.
    """
    admin_exists = db.query(User).filter(User.role == UserRole.ADMIN).first() is not None
    if admin_exists:
        return

    # Default admin for foundation (change in production)
    register_user(
        db,
        email="admin@school.local",
        full_name="Default Admin",
        password="Admin123!change",
        role=UserRole.ADMIN,
    )
