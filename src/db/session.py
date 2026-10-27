from fastapi import Depends
from typing import Annotated
from sqlmodel import Session, create_engine

from ..config import settings

database_url = f"postgresql+psycopg2://{settings.db_user}:{settings.db_pass}@{settings.db_host}:{settings.db_port}/{settings.db_name}"
engine = create_engine(database_url, echo=settings.debug)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
