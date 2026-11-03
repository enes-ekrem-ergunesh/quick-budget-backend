from fastapi import Depends
from typing import Annotated
from sqlmodel import Session, create_engine

from ..config import settings

database_url = f"postgresql+psycopg2://{settings.DB_USER}:{settings.DB_PASS}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
engine = create_engine(database_url, echo=settings.DEBUG)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
