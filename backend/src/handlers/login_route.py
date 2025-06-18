import asyncio
import logging

from fastapi import APIRouter
from starlette.responses import RedirectResponse

import config
from src.entities.entities import DBEntities
from src.models.models import UserModel

logger = logging.getLogger(__name__)

login_router = APIRouter(prefix="/login")


@login_router.post('/search')
async def login(user: UserModel):
    room = await DBEntities.rooms_control.add_participant(user)
    status = room.status
    while status != "connected":
        await asyncio.sleep(5)
        status = await DBEntities.rooms_control.get_status(room.room_id)
    return {
        "url": f"ws://{config.domain}/ws/{room.room_id}/{user.nickname}"
    }




