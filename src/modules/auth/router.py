from fastapi import APIRouter
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError

from . import service as auth_service, schemas, messages
from ...db.session import SessionDep
from ...dependencies import AuthDep
from ...core import security

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)

@router.post("/register")
async def register(register_form_data: schemas.Register, session: SessionDep):
    return auth_service.register(register_form_data, session)

@router.post("/login")
async def login(form_data: security.OAuth2PassReqDep, session: SessionDep):
    try:
      login_form_data = schemas.Login.model_validate({"email": form_data.username, "password": form_data.password})
      return auth_service.login(login_form_data, session)
    except ValidationError as e:
        raise RequestValidationError(e.errors())

@router.post("/logout")
async def logout(auth: AuthDep):
    auth_session, session = auth
    auth_service.logout(auth_session, session)
    return {"message": messages.LOGOUT_SUCCESS}