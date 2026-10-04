from sqlalchemy.orm import Session

from app.models.user import User
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
)


def create_user(db: Session, user):
    existing_user = db.query(User).filter(User.email == user.email).first()

    if existing_user:
        return {"success": False, "message": "Email already exists"}

    hashed_password = hash_password(user.password)

    db_user = User(
        username=user.username,
        email=user.email,
        password=hashed_password,
        role=user.role,
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return {"success": True, "message": "User registered successfully"}


def get_users(db: Session):
    return db.query(User).all()


def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def login_user(db: Session, email: str, password: str):
    user = db.query(User).filter(User.email == email).first()

    if not user:
        return None

    if not verify_password(password, user.password):
        return None

    access_token = create_access_token(
        {"user_id": user.id, "email": user.email, "role": user.role}
    )

    refresh_token = create_refresh_token(
        {"user_id": user.id, "email": user.email, "role": user.role}
    )

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }


def update_user_role(db, user_id, role):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        return None

    user.role = role

    db.commit()
    db.refresh(user)

    return user
def change_password(db: Session, user_id: int, current_password: str, new_password: str):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        return {
            "success": False,
            "message": "User not found"
        }

    if not verify_password(current_password, user.password):
        return {
            "success": False,
            "message": "Current password is incorrect"
        }

    user.password = hash_password(new_password)

    db.commit()
    db.refresh(user)

    return {
        "success": True,
        "message": "Password changed successfully"
    }