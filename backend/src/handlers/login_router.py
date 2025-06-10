import logging

from fastapi import APIRouter

from src.entities.entities import DBEntities
from src.models.models import UserModel

logger = logging.getLogger(__name__)

login_router = APIRouter(prefix="/login")


@login_router.post('/find')
async def login(user: UserModel):
    await DBEntities.rooms_control.add_participant(user)
    return {"sosi": "huy"}
