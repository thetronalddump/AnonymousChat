from typing import List

from pydantic import BaseModel


class UserModel(BaseModel):
    nickname: str
    age: int
    gender: str


class RoomModel(BaseModel):
    room_id: int
    status: str
    created_at: int
    expires_at: int
    participants: List[UserModel]