from sqlmodel import Session

from ..user.model import User_Account
from ..user.repository import insert_user as user_insert_user, select_user_by_email as user_select_user_by_email

def insert_user(user_account: User_Account, session: Session):
  user_insert_user(user_account, session)

def select_user_by_email(email: str, session: Session):
  return user_select_user_by_email(email, session)