from typing import Annotated

from fastapi import Depends
from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

import jwt
from jwt.exceptions import InvalidTokenError, ExpiredSignatureError
from pwdlib import PasswordHash
from pwdlib.exceptions import UnknownHashError

from . import messages
from ..config import settings
from ..modules.auth.schemas import TokenPayload

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")
password_hash = PasswordHash.recommended()


def get_password_hash(password):
    return password_hash.hash(password)


def verify_password(plain_password, hashed_password):
    try:
        return password_hash.verify(plain_password, hashed_password)
    except UnknownHashError:
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR, messages.UNKNOWN_HASH
        )


def create_token(token_payload: TokenPayload):
    encoded_jwt = jwt.encode(
        token_payload.model_dump(),
        settings.JWT_SECRET,
        algorithm=settings.JWT_ALGORITHM,
    )
    return encoded_jwt


def decode_token(token_str: str):
    try:
        return jwt.decode(
            token_str, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM]
        )
    except ExpiredSignatureError:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, messages.INVALID_TOKEN)
    except InvalidTokenError:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, messages.INVALID_TOKEN)

OAuth2PassReqDep = Annotated[OAuth2PasswordRequestForm, Depends()]
OAuth2SchemeDep = Annotated[str, Depends(oauth2_scheme)]