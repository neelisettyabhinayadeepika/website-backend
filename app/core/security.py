from datetime import datetime, timedelta, timezone
from cryptography.fernet import Fernet

from jose import jwt
from passlib.context import CryptContext

from app.core.config import FERNET_KEY
from app.core.settings import settings


# ---------------- CONFIG ----------------
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES
REFRESH_TOKEN_EXPIRE_DAYS = 7


# ---------------- PASSWORD ----------------
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


# ---------------- ENCRYPTION ----------------
cipher = Fernet(FERNET_KEY.encode())


# ---------------- ACCESS TOKEN ----------------
def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire, "type": "access"})

    # JWT CREATE
    jwt_token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    # ENCRYPT JWT
    encrypted_token = cipher.encrypt(jwt_token.encode()).decode()

    return encrypted_token


# ---------------- REFRESH TOKEN ----------------
def create_refresh_token(data: dict):
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)

    to_encode.update({"exp": expire, "type": "refresh"})

    # JWT CREATE
    jwt_token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    # ENCRYPT JWT
    encrypted_token = cipher.encrypt(jwt_token.encode()).decode()

    return encrypted_token


# ---------------- VERIFY TOKEN ----------------
def verify_token(token: str, expected_type: str = None):
    try:
        # DECRYPT FIRST
        jwt_token = cipher.decrypt(token.encode()).decode()

        # VERIFY JWT
        payload = jwt.decode(jwt_token, SECRET_KEY, algorithms=[ALGORITHM])

        # CHECK TYPE
        token_type = payload.get("type")

        if expected_type and token_type != expected_type:
            return None

        return payload

    except Exception as e:
        print("TOKEN ERROR:", str(e))
        return None
