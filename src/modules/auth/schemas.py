from pydantic import BaseModel, EmailStr
from datetime import datetime

class Register(BaseModel):
    email: EmailStr
    password: str

class Login(BaseModel):
    email: EmailStr # used 'username' instead of 'email' because of OAuth2 restrictions
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenPayload(BaseModel):
    sub: str
    iat: datetime
    exp: datetime