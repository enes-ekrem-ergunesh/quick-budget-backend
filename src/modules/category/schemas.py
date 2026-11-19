import uuid
from pydantic import BaseModel

class PostCategory(BaseModel):
    title: str
    emoji: str

class PatchCategory(BaseModel):
    id: uuid.UUID
    title: str | None
    emoji: str | None