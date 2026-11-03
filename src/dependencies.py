import uuid
from typing import Annotated
from fastapi import Depends, HTTPException
from . import messages
from .core import security
from .db import session
from .modules.auth.schemas import TokenPayload
from .modules.auth.models import Auth_Session
from .modules.auth.repository import get_session_by_id


def get_current_auth_session(
    token_str: security.OAuth2SchemeDep, session: session.SessionDep
):
    token_decoded = security.decode_token(token_str)
    token_payload = TokenPayload.model_validate(token_decoded)
    session_id = uuid.UUID(hex=token_payload.sub)
    auth_session: Auth_Session | None = get_session_by_id(session_id, session)
    if not auth_session:
        raise HTTPException(401, messages.SESSION_MISSING)
    if auth_session.revoked_at:
        raise HTTPException(401, messages.SESSION_REVOKED)

    return auth_session, session


AuthDep = Annotated[tuple[Auth_Session, session.SessionDep], Depends(get_current_auth_session)]
