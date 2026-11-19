import uuid
from fastapi import APIRouter
from . import service, schemas
from ...dependencies import AuthDep

router = APIRouter(
    prefix="/entry",
    tags=["entry"],
)


@router.get("/")
async def get_user_entries(auth: AuthDep):
    auth_session, _ = auth
    return service.get_user_entries(auth_session)

@router.get("/{entry_id}")
async def get_user_entry_by_id(entry_id: uuid.UUID, auth: AuthDep):
    auth_session, _ = auth
    return service.get_user_entry_by_id(entry_id, auth_session)

@router.post("/")
async def post_entry(new_entry: schemas.PostEntry, auth: AuthDep):
    auth_session, session = auth
    return service.post_entry(auth_session, new_entry, session)

@router.patch("/")
async def put_entry(entry: schemas.PatchEntry, auth: AuthDep):
    auth_session, session = auth
    return service.patch_entry(auth_session, entry, session)

@router.delete("/{entry_id}")
async def delete_entry(entry_id: uuid.UUID, auth: AuthDep):
    auth_session, session = auth
    return service.delete_entry(auth_session, entry_id, session)
