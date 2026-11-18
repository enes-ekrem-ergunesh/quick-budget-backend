import uuid
from pydantic import BaseModel
from .models import EntryType

class PostEntry(BaseModel):
    category_id: uuid.UUID | None = None
    title: str
    amount: float | None = None
    currency: str | None = None
    type: EntryType | None = None


class PutEntry(BaseModel):
    id: uuid.UUID
    category_id: uuid.UUID | None = None
    title: str | None = None
    amount: float | None = None
    currency: str | None = None
    type: EntryType | None = None