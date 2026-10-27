from fastapi import APIRouter
from .messages import *
from .schemas import Register
from . import service as auth_service
from ...db.session import SessionDep

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)

@router.post("/register")
async def register(body: Register, session: SessionDep):
    return auth_service.register(body, session)