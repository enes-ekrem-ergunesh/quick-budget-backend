import uuid
from fastapi import APIRouter
from . import service, schemas
from ...dependencies import AuthDep

router = APIRouter(
    prefix="/category",
    tags=["category"],
)


@router.get("/")
async def get_user_categories(auth: AuthDep):
    auth_session, _ = auth
    return service.get_user_categories(auth_session)

@router.get("/{category_id}")
async def get_user_category_by_id(category_id: uuid.UUID, auth: AuthDep):
    auth_session, _ = auth
    return service.get_user_category_by_id(category_id, auth_session)

@router.post("/")
async def post_category(new_category: schemas.PostCategory, auth: AuthDep):
    auth_session, session = auth
    return service.post_category(auth_session, new_category, session)

@router.patch("/")
async def put_category(category: schemas.PatchCategory, auth: AuthDep):
    auth_session, session = auth
    return service.patch_category(auth_session, category, session)

@router.delete("/{category_id}")
async def delete_category(category_id: uuid.UUID, auth: AuthDep):
    auth_session, session = auth
    return service.delete_category(auth_session, category_id, session)