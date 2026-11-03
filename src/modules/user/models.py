import uuid
from typing import TYPE_CHECKING
from datetime import datetime, UTC
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from .dependencies import Auth_Session

class User_Account(SQLModel, table=True):
  id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
  email: str = Field(index=True)
  password_hash: str = Field()
  created_at: datetime = Field(default=datetime.now(UTC))
  updated_at: datetime | None = Field(default=None)

  auth_sessions: list["Auth_Session"] = Relationship(back_populates="user_account")