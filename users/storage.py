from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError

from users.models import User
from users.schemas import UserCreate
from users.security import hash_password

def get_user_by_email(email: str, db: Session) -> User | None:
    return db.query(User).filter(User.email == email).first()

def create_user(
        user: UserCreate,
        db: Session
) -> User:
    new_user = User(
        name=user.name,
        email=user.email,
        password_hash=hash_password(user.password)
    )
    db.add(new_user)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered"
        )

    db.refresh(new_user)
    return new_user

def get_current_user() -> User:
    ...