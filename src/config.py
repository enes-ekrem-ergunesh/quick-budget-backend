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
    DEBUG: bool = os.getenv("FASTAPI_ENV", "development") == "development"
    DB_HOST: str = "127.0.0.1" if DEBUG else "db"
    DB_PORT: int = int(os.getenv("POSTGRES_HOST_PORT", "5432"))
    DB_USER: str | None = os.getenv("POSTGRES_USER")
    DB_PASS: str | None = os.getenv("POSTGRES_PASSWORD")
    DB_NAME: str | None = os.getenv("POSTGRES_DB")
    JWT_SECRET: str | None = os.getenv("JWT_SECRET")
    JWT_ALGORITHM: str = 'HS256'
    ACCESS_TOKEN_TTL: int = 60

    if DB_USER is None: raise_for_missing("db_user")
    if DB_PASS is None: raise_for_missing("db_pass")
    if DB_NAME is None: raise_for_missing("db_name")
    if JWT_SECRET is None: raise_for_missing("jwt_secret")


settings = Settings()