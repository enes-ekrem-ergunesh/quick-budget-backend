import uuid
from enum import Enum
from typing import TYPE_CHECKING, Optional
from datetime import datetime, UTC
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from ..user.models import User_Account
    from ..category.models import Category

class EntryType(str, Enum):
   income = "income"
   expense = "expense"
  

class Entry(SQLModel, table=True):
  id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
  user_id: uuid.UUID = Field(foreign_key="user_account.id")
  category_id: uuid.UUID | None = Field(default=None, foreign_key="category.id")
  title: str = Field()
  amount: float | None = Field(default=None)
  currency: str | None = Field(default=None)
  type: EntryType | None = Field(default=None)
  created_at: datetime = Field(default=datetime.now(UTC))
  updated_at: datetime | None = Field(default=None)

  user_account: "User_Account" = Relationship(back_populates="entries")
  category: Optional["Category"] = Relationship(back_populates="entries")