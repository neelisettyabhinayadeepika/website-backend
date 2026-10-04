from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from app.core.database import get_db
from app.models.user import User
from middleware.jwt import create_token

router = APIRouter()

pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post("/login")
def login(email: str, password: str, response: Response, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email).first()

    if not user:
        raise HTTPException(400, "Invalid credentials")

    if not pwd.verify(password, user.password):
        raise HTTPException(400, "Wrong password")

    
    token = create_token(
        {
            "user_id": user.id,
            "email": user.email,
            "role": user.role, 
        }
    )

    response.set_cookie(
        key="access_token", value=token, httponly=True, samesite="Lax", secure=False
    )

    return {
        "message": "Login successful",
        "role": user.role,  
    }
