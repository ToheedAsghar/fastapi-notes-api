from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from database import get_db
from users.models import User
from users.schemas import Token, UserCreate, UserResponse
from users.storage import get_user_by_email, create_user
from users.security import create_access_token, verify_password

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def register(
    user: UserCreate,
    db: Annotated[Session, Depends(get_db)],
) -> User:
    return create_user(user, db)

@router.post("/login", response_model=Token)
def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Annotated[Session, Depends(get_db)],
) -> Token:
    user = get_user_by_email(form_data.username, db)

    if user is None or verify_password(form_data.password, str(user.password_hash)):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    token = create_access_token(int(user.id))
    return Token(access_token=token)
