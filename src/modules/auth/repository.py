import uuid
from sqlmodel import Session, select
from datetime import datetime, UTC

from .models import Auth_Session

def insert_session(auth_session: Auth_Session, session: Session):
  session.add(auth_session)

def get_session_by_id(session_id: uuid.UUID, session: Session):
  return session.get(Auth_Session, session_id)

def revoke_session(auth_session: Auth_Session, session: Session):
  auth_session.revoked_at = datetime.now(UTC)
  session.add(auth_session)
