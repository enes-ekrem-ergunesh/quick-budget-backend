import uuid
from typing import TYPE_CHECKING
from datetime import datetime, UTC
from sqlmodel import SQLModel, Field, Relationship
from ..entry.models import Entry

if TYPE_CHECKING:
    from ..user.models import User_Account

class Category(SQLModel, table=True):
  id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
  user_id: uuid.UUID = Field(foreign_key="user_account.id")
  title: str = Field()
  emoji: str = Field()
  created_at: datetime = Field(default=datetime.now(UTC))
  updated_at: datetime | None = Field(default=None)

  user_account: "User_Account" = Relationship(back_populates="categories")
  entries: list["Entry"] = Relationship(back_populates="category")

class Default_Category(SQLModel, table=True):
  id: int = Field(primary_key=True)
  title: str = Field(unique=True)
  emoji: str = Field()
  created_at: datetime = Field()
  updated_at: datetime | None = Field()