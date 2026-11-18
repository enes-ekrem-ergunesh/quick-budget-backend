import uuid
from fastapi import HTTPException
from sqlmodel import Session, select
from . import models, schemas, messages
from ..auth.models import Auth_Session
from ..default.schemas import DetailResponse


def get_user_categories(auth_session: Auth_Session):
    return auth_session.user_account.categories

def get_user_category_by_id(category_id: uuid.UUID, auth_session: Auth_Session):
    category = [category for category in auth_session.user_account.categories if category.id == category_id]
    if len(category) == 0:
        HTTPException(404, messages.CATEGORY_NOT_FOUND)
    return category[0]


def post_category(
    auth_session: Auth_Session, new_category: schemas.PostCategory, session: Session
):
    category = models.Category(
        id=uuid.uuid4(),
        user_id=auth_session.user_account.id,
        title=new_category.title,
        emoji=new_category.emoji,
    )
    session.add(category)
    session.commit()
    session.refresh(category)
    return category


def put_category(
    auth_session: Auth_Session, put_category: schemas.PutCategory, session: Session
):
    category = session.get(models.Category, put_category.id)
    if not category:
        raise HTTPException(404, "Category not found")
    if category.user_account != auth_session.user_account:
        raise HTTPException(403, "You should own the category to update it")
    if put_category.title:
        category.title = put_category.title
    if put_category.emoji:
        category.emoji = put_category.emoji
    session.add(category)
    session.commit()
    session.refresh(category)
    return category


def delete_category(
    auth_session: Auth_Session, category_id: uuid.UUID, session: Session
):
    category = session.get(models.Category, category_id)
    if not category:
        raise HTTPException(404, "Category not found")
    if category.user_account != auth_session.user_account:
        raise HTTPException(403, "You should own the category to delete it")
    session.delete(category)
    session.commit()
    return DetailResponse(detail="Category deleted successfully")


def import_default_categories(user_id: uuid.UUID, session: Session):
    default_categories = session.exec(select(models.Default_Category))
    for default_category in default_categories:
        session.add(
            models.Category(
                id=uuid.uuid4(),
                user_id=user_id,
                title=default_category.title,
                emoji=default_category.emoji,
            )
        )
