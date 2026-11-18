import uuid
from fastapi import HTTPException
from sqlmodel import Session
from ..auth.models import Auth_Session
from . import models, schemas
from ..default.schemas import DetailResponse
from ..category.models import Category
from ...core.currency import get_currency


def get_user_entries(auth_session: Auth_Session):
    return auth_session.user_account.entries


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
    if new_entry.currency:
        entry.currency = get_currency(new_entry.currency)
    session.add(entry)
    session.commit()
    session.refresh(entry)
    return entry


def put_entry(
    auth_session: Auth_Session, put_entry: schemas.PutEntry, session: Session
):
    entry = session.get(models.Entry, put_entry.id)
    if not entry:
        raise HTTPException(404, "Entry not found")
    if entry.user_account != auth_session.user_account:
        raise HTTPException(403, "You should own the entry to update it")
    if put_entry.title:
        entry.title = put_entry.title
    if put_entry.category_id:
        category = session.get(Category, put_entry.category_id)
        if category:
            entry.category_id = category.id
    if put_entry.amount:
        entry.amount = put_entry.amount
    if put_entry.currency:
        entry.currency = put_entry.currency
    if put_entry.type:
        entry.type = put_entry.type
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
