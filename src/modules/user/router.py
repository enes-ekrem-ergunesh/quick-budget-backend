from fastapi import APIRouter
from .messages import *

router = APIRouter(tags=["user"])

@router.get("/")
async def root():
    return {"message": ""}