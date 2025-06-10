import logging
import time
from typing import List, Dict

import redis.asyncio as redis
from redis.asyncio import Redis

from src.models.models import UserModel
from utils.utils import find_best_room

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

    async def _create_room(
            self,
            user: UserModel
    ):
        if not self.__con:
            await self.__create_connection()

        try:
            logger.info("Creating room for user %s", user.nickname)
            async with self.__con.pipeline() as connection:
                next_id = await connection.incr("room:id")
                key = f"user:{next_id}"
                value = {
                    "status": "waiting",
                    "created_at": time.time(),
                    "expires_at": time.time() + EXPIRATION_TIME,
                    "participants": [
                        {
                            "nickname": user.nickname,
                             "age": user.age,
                             "gender": user.gender,
                         }
                    ]
                }
                await connection.set(key, value).execute()
                await connection.expire(key, EXPIRATION_TIME).execute()
            logger.info("Done creating room for user %s", user.nickname)
            return True
        except Exception as e:
            logger.error("Error while creating room for user %d", user.nickname, exc_info=e)

    async def _get_rooms(self) -> List[Dict] | List[None]:
        if not self.__con:
            await self.__create_connection()

        try:
            logger.info("Getting rooms from cache")
            async with self.__con.pipeline() as connection:
                keys = await connection.keys().execute()
                rooms = []
                for key in keys:
                    room = await connection.get(key).execute()
                    rooms.append(room)

            logger.info("Done getting rooms from cache, total rooms: %d", len(rooms))
            return rooms if len(rooms) > 0 else [None]
        except Exception as e:
            logger.error("Error while reading from cache", exc_info=e)
            return [None]

    async def add_participant(self, user: UserModel):
        if not self.__con:
            await self.__create_connection()

        try:
            logger.info("Adding participant &s to room ", user.nickname)
            async with self.__con.pipeline() as connection:
                rooms = await self._get_rooms()
                best_room = find_best_room(user, rooms)
                if best_room:
                    best_room["participants"][user.nickname] = {
                        "gender": user.gender,
                        "age": user.age,
                    }
                    key = f"user:{await connection.incr("user:id")}"
                    await connection.set(key, best_room).execute()
                else:
                    await self._create_room(user)
            logger.info("Done adding participant &s to room ", user.nickname)
        except Exception as e:
            logger.error("Error while adding participant &s to room ", user.nickname, exc_info=e)
