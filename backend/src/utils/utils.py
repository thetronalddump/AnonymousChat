import json
from typing import List

from src.models.models import UserModel, RoomModel


def find_best_room(current_user: UserModel, rooms: List[RoomModel]):
    best_match = None
    min_age_diff = float('inf')
    if rooms:
        for room in rooms:
            room = RoomModel.model_validate(json.loads(room[0]))
            if room.status == "waiting":
                user = room.participants[0]
                if user.gender != current_user.gender:
                    age_diff = abs(user.age - current_user.age)
                    if age_diff < min_age_diff:
                        min_age_diff = age_diff
                        best_match = room

    return best_match if best_match else False