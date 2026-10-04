from fastapi import APIRouter, Depends, HTTPException, Response, Request
from sqlalchemy.orm import Session

from app.core.auth import get_current_user, role_required
from app.core.database import get_db
from app.core.security import (
    create_access_token,
    create_refresh_token,
    verify_token,
)
from app.models.user import User


from app.schemas.user_schema import UserCreate, UserLogin,ChangePassword
from app.services.user_service import (
    create_user,
    login_user,
    get_users,
    get_user_by_id,
    update_user_role,
    change_password,
)
from app.schemas.user_schema import EditProfile

router = APIRouter(prefix="/users", tags=["Users"])


# VERIFY USER
@router.get("/verify")
def verify(current_user=Depends(get_current_user)):
    return {
        "authenticated": True,
        "role": current_user.role,
    }


# REGISTER
@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    return create_user(db, user)


# LOGIN
@router.post("/login")
def login(user: UserLogin, response: Response, db: Session = Depends(get_db)):
    token = login_user(db, user.email, user.password)

    if not token:
        raise HTTPException(status_code=401, detail="Invalid email or password")

    response.set_cookie(
        key="access_token",
        value=token["access_token"],
        httponly=True,
        secure=False,
        samesite="Lax",
    )

    response.set_cookie(
        key="refresh_token",
        value=token["refresh_token"],
        httponly=True,
        secure=False,
        samesite="Lax",
    )

    return {"message": "Login successful"}


# REFRESH TOKEN
@router.post("/refresh")
def refresh_token(
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
):
    refresh_token = request.cookies.get("refresh_token")

    if not refresh_token:
        raise HTTPException(status_code=401, detail="Refresh token missing")

    payload = verify_token(refresh_token)

    if not payload or payload.get("type") != "refresh":
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    user = get_user_by_id(db, payload["user_id"])

    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    access_token = create_access_token(
        {
            "user_id": user.id,
            "email": user.email,
            "role": user.role,
        }
    )

    refresh_token = create_refresh_token(
        {
            "user_id": user.id,
            "email": user.email,
            "role": user.role,
        }
    )

    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=False,
        samesite="Lax",
    )

    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=False,
        samesite="Lax",
    )

    return {"message": "Token refreshed successfully"}


# CURRENT USER
@router.get("/me")
def get_me(current_user=Depends(get_current_user)):
    return {
        "id": current_user.id,
        "username": current_user.username,
        "email": current_user.email,
        "role": current_user.role,
    }


# GET ALL USERS (SUPERADMIN ONLY)
@router.get("/admin/users")
def admin_users(
    db: Session = Depends(get_db), current_user=Depends(role_required(["superadmin"]))
):
    return get_users(db)


# UPDATE USER ROLE (SUPERADMIN ONLY)
@router.put("/admin/role/{user_id}")
def change_role(
    user_id: int,
    role: str,
    db: Session = Depends(get_db),
    current_user=Depends(role_required(["superadmin"])),
):
    user = update_user_role(db, user_id, role)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return {
        "message": "Role updated successfully",
        "user_id": user.id,
        "role": user.role,
    }


# USER + SUPERADMIN ACCESS
@router.get("/profile")
def profile(current_user=Depends(role_required(["user", "superadmin"]))):
    return {
        "message": "Profile access granted",
        "user": current_user.username,
        "role": current_user.role,
    }


# =========================
# EDIT PROFILE (USER)
# =========================
@router.put("/editprofile")
def edit_profile(
    data: EditProfile,
    db: Session = Depends(get_db),
    current_user=Depends(role_required(["user", "superadmin"])),
):
    user = get_user_by_id(db, current_user.id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Update username
    if data.username is not None:
        user.username = data.username

    # Update email
    if data.email is not None:
        user.email = data.email

    db.commit()
    db.refresh(user)

    return {
        "message": "Profile updated successfully",
        "user": {"id": user.id, "username": user.username, "email": user.email},
    }


# GET ALL USERS
@router.get("/")
def get_all_users(
    db: Session = Depends(get_db), current_user=Depends(role_required(["superadmin"]))
):
    return get_users(db)


# GET USER BY ID
@router.get("/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = get_user_by_id(db, user_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user


@router.delete("/{id}")
def delete_user(
    id: int,
    db: Session = Depends(get_db),
    current_user=Depends(role_required(["superadmin"])),
):
    user = db.query(User).filter(User.id == id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(user)
    db.commit()

    return {"message": "User deleted successfully"}

@router.put("/change-password")
def update_password(
    data: ChangePassword,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    result = change_password(
        db,
        current_user.id,
        data.current_password,
        data.new_password,
    )

    if not result["success"]:
        raise HTTPException(
            status_code=400,
            detail=result["message"],
        )

    return result


@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie("access_token", path="/")
    response.delete_cookie("refresh_token", path="/")  # Remove if you don't use it

    return {"success": True, "message": "Logged out successfully"}
