import asyncio
import logging

from fastapi import APIRouter

import config
from src.entities.entities import DBEntities
from src.models.models import UserModel

logger = logging.getLogger(__name__)

login_router = APIRouter(prefix="/login")


@login_router.post("/search")
async def login(user: UserModel):
    room = await DBEntities.rooms_control.add_participant(user)
    status = room.status
    while status != "connected" and status != "deleted":
        await asyncio.sleep(5)
        status = await DBEntities.rooms_control.get_status(room.room_id)
    if status == "connected":
        companion_info = await DBEntities.rooms_control.get_companion_info(
            room.room_id, user
        )
        response = {
            "url": f"ws://{config.domain}/ws/{room.room_id}/{user.nickname}",
            "companion_info": companion_info,
        }
    else:
        response = {
            "message": "the search was canceled successfully"
        }
    return response


@login_router.post("/close")
async def close_search(user: UserModel) -> dict[str, str]:
    room_id = await DBEntities.rooms_control.find_participant(user)
    await DBEntities.rooms_control.delete_room(room_id)

    return {"status": "closed"}
