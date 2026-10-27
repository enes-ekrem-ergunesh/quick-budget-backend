from sqlmodel import SQLModel, Field
from datetime import datetime, UTC

class User_Account(SQLModel, table=True):
  id: int | None = Field(default=None, primary_key=True)
  email: str = Field(index=True)
  password_hash: str = Field()
  created_at: datetime = Field(default=datetime.now(UTC))
  updated_at: datetime | None = Field(default=None)