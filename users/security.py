import bcrypt
from typing import Annotated
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta, timezone
from fastapi import Depends, HTTPException, status

from database import get_db
from users.models import User
from notes.models import Note

SECRET_KEY = "dev-secret-do-not-use-in-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def get_current_user(
        token: Annotated[str, Depends(oauth2_scheme)],
        db: Annotated[Session, Depends(get_db)]
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )
    try:
        payload = jwt.decode(
            token, SECRET_KEY, algorithms=[ALGORITHM]
        )
        user_id_str : str | None = payload.get("sub")

        if user_id_str is None:
            raise credentials_exception
        user_id = int(user_id_str)
    except (JWTError, ValueError):
        raise credentials_exception

    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise credentials_exception
    return user

def hash_password(plain_password: str) -> str:
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(plain_password.encode("utf-8"), salt)
    return hashed.decode("utf-8")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(
        plain_password.encode("utf-8"),
        hashed_password.encode("utf-8")
    )

def create_access_token(
        user_id: int
) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    payload = {
        "sub": str(user_id),
        "exp": expire
    }

    return jwt.encode(payload, SECRET_KEY, ALGORITHM)
