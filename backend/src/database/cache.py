import json
import logging
import time

import redis.asyncio as redis
from redis.asyncio import Redis

from src.models.models import RoomModel, UserModel
from src.utils.utils import find_best_room

logger = logging.getLogger(__name__)


EXPIRATION_TIME = 600


class RedisConnection:
    __con: Redis | None = None

    def __init__(self, init_data: dict):
        self.__init_data = init_data

    @staticmethod
    def __create_connection(redis_data: dict):
        try:
            RedisConnection.__con = redis.from_url(**redis_data)
        except Exception as e:
            logger.error("Can't connect to redis server", exc_info=e)

    @staticmethod
    async def get_connection(redis_data: dict) -> Redis:
        if not RedisConnection.__con:
            RedisConnection.__create_connection(redis_data)
        return RedisConnection.__con


class RoomsControl:
    def __init__(self, init_data: dict):
        self.__con: Redis | None = None
        self.__init_data = init_data

    async def __create_connection(self):
        self.__con = await RedisConnection.get_connection(self.__init_data)

    async def _create_room(self, user: UserModel):
        if not self.__con:
            await self.__create_connection()

        try:
            logger.info("Creating room for user %s", user.nickname)
            async with self.__con.pipeline() as connection:
                next_id = await connection.incr("room:id").execute()
                key = f"room:{next_id[0]}"
                value = {
                    "room_id": next_id[0],
                    "status": "waiting",
                    "created_at": int(time.time()),
                    "expires_at": int(time.time() + EXPIRATION_TIME),
                    "participants": [
                        {
                            "nickname": user.nickname,
                            "age": user.age,
                            "gender": user.gender,
                        }
                    ],
                }
                await connection.set(key, json.dumps(value)).execute()
                await connection.expire(key, EXPIRATION_TIME).execute()

            logger.info("Done creating room for user %s", user.nickname)
            return RoomModel.model_validate(value)
        except Exception as e:
            logger.error(
                "Error while creating room for user %s", user.nickname, exc_info=e
            )

    async def _get_rooms(self) -> list[dict] | list[None]:
        if not self.__con:
            await self.__create_connection()

        try:
            logger.info("Getting rooms from cache")
            async with self.__con.pipeline() as connection:
                keys = await connection.keys().execute()
                keys = keys[0]
                rooms = []
                for key in keys:
                    if key != "room:id":
                        room = await connection.get(key).execute()
                        rooms.append(room)

            logger.info("Done getting rooms from cache, total rooms: %d", len(rooms))
            return rooms if len(rooms) > 0 else None
        except Exception as e:
            logger.error("Error while reading from cache", exc_info=e)
            return None

    async def add_participant(self, user: UserModel):
        if not self.__con:
            await self.__create_connection()

        try:
            logger.info("Adding participant %s to room ", user.nickname)
            async with self.__con.pipeline() as connection:
                rooms = await self._get_rooms()
                best_room = find_best_room(user, rooms)
                if best_room:
                    best_room.participants.append(user.model_dump())
                    best_room.status = "connected"
                    key = f"room:{best_room.room_id}"
                    await connection.set(
                        key, json.dumps(best_room.model_dump())
                    ).execute()
                    logger.info("Done adding participant %s to room ", user.nickname)
                    return best_room
                else:
                    return await self._create_room(user)

        except Exception as e:
            logger.error(
                "Error while adding participant %s to room ", user.nickname, exc_info=e
            )

    async def get_status(self, room_id: int):
        if not self.__con:
            await self.__create_connection()

        try:
            logger.info("Getting room from cache, id: %s", room_id)
            async with self.__con.pipeline() as connection:
                room = await connection.get(f"room:{room_id}").execute()
                status = json.loads(room[0])["status"]
                return status
        except Exception as e:
            logger.error("Error while getting room from cache", exc_info=e)
            return None

    async def get_companion_info(self, room_id, user):
        if not self.__con:
            await self.__create_connection()

        try:
            logger.info("Getting room from cache, id: %s", room_id)
            async with self.__con.pipeline() as connection:
                room = await connection.get(f"room:{room_id}").execute()
                participants = json.loads(room[0])["participants"]
                companion = [
                    participant
                    for participant in participants
                    if participant["nickname"] != user.nickname
                ][0]
                return companion
        except Exception as e:
            logger.error("Error while getting room from cache", exc_info=e)
            return None

    async def delete_room(self, room_id):
        if not self.__con:
            await self.__create_connection()

        try:
            logger.info("Deleting room from cache, id: %s", room_id)
            async with self.__con.pipeline() as connection:
                await connection.delete(f"room:{room_id}").execute()
        except Exception as e:
            logger.error("Error while deleting room from cache", exc_info=e)
