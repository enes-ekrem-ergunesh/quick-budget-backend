from sqlmodel import Session, select
from .model import User_Account


def insert_user(user_account: User_Account, session: Session):
  try:
    session.add(user_account)
  except Exception as e:
    raise e

def select_user_by_email(email: str, session: Session):
  statement = select(User_Account).where(User_Account.email == email)
  result = session.exec(statement)
  return result.one_or_none()