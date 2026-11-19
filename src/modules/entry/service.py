import uuid
from fastapi import HTTPException
from sqlmodel import Session
from ..auth.models import Auth_Session
from . import models, schemas, messages
from ..default.schemas import DetailResponse
from ..category.models import Category
from ...core.currency import get_currency


def get_user_entries(auth_session: Auth_Session):
    return auth_session.user_account.entries

def get_user_entry_by_id(entry_id: uuid.UUID, auth_session: Auth_Session):
    entry = [x for x in auth_session.user_account.entries if x.id == entry_id]
    if len(entry) == 0:
        HTTPException(404, messages.ENTRY_NOT_FOUND)
    return entry[0]


def post_entry(
    auth_session: Auth_Session, new_entry: schemas.PostEntry, session: Session
):
    entry = models.Entry(
        id=uuid.uuid4(), user_id=auth_session.user_account.id, title=new_entry.title
    )
    if new_entry.category_id:
        category = session.get(Category, new_entry.category_id)
        if category:
            entry.category_id = category.id
        else:
            raise HTTPException(404, "Category not found")
    entry.amount = new_entry.amount
    entry.type = new_entry.type
    entry.entry_date = new_entry.entry_date
    entry.entry_time = new_entry.entry_time
    entry.note = new_entry.note
    if new_entry.currency:
        entry.currency = get_currency(new_entry.currency)
    session.add(entry)
    session.commit()
    session.refresh(entry)
    return entry


def patch_entry(
    auth_session: Auth_Session, patch_entry: schemas.PatchEntry, session: Session
):
    entry = session.get(models.Entry, patch_entry.id)
    if not entry:
        raise HTTPException(404, "Entry not found")
    if entry.user_account != auth_session.user_account:
        raise HTTPException(403, "You should own the entry to update it")
    if patch_entry.title:
        entry.title = patch_entry.title
    if patch_entry.category_id:
        category = session.get(Category, patch_entry.category_id)
        if category:
            entry.category_id = category.id
    if patch_entry.amount:
        entry.amount = patch_entry.amount
    if patch_entry.currency:
        entry.currency = patch_entry.currency
    if patch_entry.type:
        entry.type = patch_entry.type
    if patch_entry.entry_date:
        entry.entry_date = patch_entry.entry_date
    if patch_entry.entry_time:
        entry.entry_time = patch_entry.entry_time
    if patch_entry.note:
        entry.note = patch_entry.note
    session.add(entry)
    session.commit()
    session.refresh(entry)
    return entry


def delete_entry(auth_session: Auth_Session, entry_id: uuid.UUID, session: Session):
    entry = session.get(models.Entry, entry_id)
    if not entry:
        raise HTTPException(404, "Entry not found")
    if entry.user_account != auth_session.user_account:
        raise HTTPException(403, "You should own the Entry to delete it")
    session.delete(entry)
    session.commit()
    return DetailResponse(detail="Entry deleted successfully")
