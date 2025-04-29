from sqlalchemy.orm import Session
from app.schemas.user import UserLogin
from app.crud.user import get_user_by_email
from app.core.security import verify_password, create_access_token

def authenticate_user(db: Session, login_data: UserLogin):
    user = get_user_by_email(db, login_data.email)
    if not user:
        return None
    if not verify_password(login_data.password, user.hashed_password):
        return None
    return user

def login_user(user):
    return create_access_token(subject=user.email)
