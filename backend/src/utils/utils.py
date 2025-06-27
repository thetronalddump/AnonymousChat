import json

from src.models.models import RoomModel, UserModel


def find_best_room(current_user: UserModel, rooms: list[list[str]] | None) -> RoomModel | bool:
    best_match = None
    min_age_diff = float("inf")
    print(rooms)
    if rooms:
        for room in rooms:
            validated_room = RoomModel.model_validate(json.loads(room[0]))
            if validated_room.status == "waiting":
                user = validated_room.participants[0]
                if user.gender != current_user.gender:
                    age_diff = abs(user.age - current_user.age)
                    if age_diff < min_age_diff:
                        min_age_diff = age_diff
                        best_match = validated_room

    return best_match if best_match else False
