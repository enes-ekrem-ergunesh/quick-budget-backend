import uuid
from datetime import datetime, UTC
from typing import TYPE_CHECKING, Optional
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from .dependencies import User_Account

class Auth_Session(SQLModel, table=True):
  id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
  user_id: uuid.UUID = Field(foreign_key="user_account.id")
  expires_at: datetime | None = Field(default=None)
  revoked_at: datetime | None = Field(default=None)
  created_at: datetime = Field(default=datetime.now(UTC))

  user_account: Optional["User_Account"] = Relationship(back_populates="auth_sessions")