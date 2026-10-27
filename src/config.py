import os
from pathlib import Path
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

from .messages import *

"""
For debugging, load the .env file from the root project directory (../../.env).

In production, env variables will be defined in the system by docker.
"""
dotenv_path = Path(__file__).resolve().parent.parent.parent / '.env'
load_dotenv(dotenv_path=dotenv_path)

def raise_for_missing(name: str):
   raise Exception(ENV_VAR_MISSING.format(name));
        
class Settings(BaseSettings):
    debug: bool = os.getenv("FASTAPI_ENV", "development") == "development"
    db_host: str = "127.0.0.1" if debug else "db"
    db_port: int = int(os.getenv("POSTGRES_HOST_PORT", "5432"))
    db_user: str | None = os.getenv("POSTGRES_USER")
    db_pass: str | None = os.getenv("POSTGRES_PASSWORD")
    db_name: str | None = os.getenv("POSTGRES_DB")

    if db_user is None: raise_for_missing("db_user")
    if db_pass is None: raise_for_missing("db_pass")
    if db_name is None: raise_for_missing("db_name")


settings = Settings()