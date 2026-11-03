import uuid
from sqlmodel import Session
from fastapi import HTTPException, status
from datetime import datetime, timedelta, UTC

from . import messages, repository, schemas, models
from ...core import security
from ...config import settings
from .dependencies import User_Account, insert_user, select_user_by_email


def register(body: schemas.Register, session: Session):
    # Validate email unique
    existing_user = select_user_by_email(body.email, session)
    if existing_user:
        raise HTTPException(
            status.HTTP_409_CONFLICT, messages.ERROR_REGISTER_EMAIL_EXISTS
        )
    # Create user
    user_id = uuid.uuid4()
    password_hash = security.get_password_hash(body.password)
    user_account = User_Account(
        id=user_id, email=body.email, password_hash=password_hash
    )
    insert_user(user_account, session)

    # Create session and access token
    access_token = create_session_and_token(user_id=user_id, session=session)

    session.commit()
    return schemas.Token(access_token=access_token, token_type="bearer")


def login(body: schemas.Login, session: Session):
    user = select_user_by_email(email=body.email, session=session)
    # Verify user
    if not user or not user.id:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED, messages.ERROR_EMAIL_NOT_REGISTERED
        )
    # Verify password
    if not security.verify_password(body.password, user.password_hash):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, messages.ERROR_WRONG_PASSWORD)

    # Create session and access token
    access_token = create_session_and_token(user_id=user.id, session=session)

    session.commit()
    return schemas.Token(access_token=access_token, token_type="bearer")


def create_session_and_token(user_id: uuid.UUID, session: Session):
    session_uuid = uuid.uuid4()
    expires_at = datetime.now(UTC) + timedelta(minutes=settings.ACCESS_TOKEN_TTL)

    # Create session
    auth_session = models.Auth_Session(
        id=session_uuid,
        user_id=user_id,
        expires_at=expires_at,
    )

    # Insert session
    repository.insert_session(auth_session, session)

    # Create access token
    access_token_payload = schemas.TokenPayload(
        sub=session_uuid.hex, iat=datetime.now(UTC), exp=expires_at
    )
    access_token = security.create_token(access_token_payload)

    return access_token


def logout(auth_session: models.Auth_Session, session: Session):
    repository.revoke_session(auth_session, session)
    session.commit()

