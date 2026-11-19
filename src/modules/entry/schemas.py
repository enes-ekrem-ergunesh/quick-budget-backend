import uuid
from datetime import date, time
from pydantic import BaseModel
from .models import EntryType

class PostEntry(BaseModel):
    category_id: uuid.UUID | None = None
    title: str
    amount: float | None = None
    currency: str | None = None
    type: EntryType | None = None
    entry_date: date | None = None
    entry_time: time | None = None
    note: str | None = None


class PatchEntry(BaseModel):
    id: uuid.UUID
    category_id: uuid.UUID | None = None
    title: str | None = None
    amount: float | None = None
    currency: str | None = None
    type: EntryType | None = None
    entry_date: date | None = None
    entry_time: time | None = None
    note: str | None = None