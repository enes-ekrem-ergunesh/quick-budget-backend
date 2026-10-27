from fastapi import APIRouter
from .messages import *

router = APIRouter(tags=["default"])

@router.get("/")
async def root():
    return {"message": ROOT_RUNNING}