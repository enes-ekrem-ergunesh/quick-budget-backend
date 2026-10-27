from sqlmodel import Session
from fastapi import HTTPException, status

from .messages import *
from .schemas import Register
from .dependencies import User_Account, insert_user, select_user_by_email

def register(body: Register, session: Session):
  # Validate email unique
  existing_user = select_user_by_email(body.email, session)
  if existing_user:
    raise HTTPException(status.HTTP_409_CONFLICT, ERROR_REGISTER_EMAIL_EXISTS)

  user_account = User_Account(email=body.email, password_hash="fakepasswordhash")
  insert_user(user_account, session)
  session.commit()
  session.refresh(user_account)
  return user_account