from decouple import config

from src.utils.ws_manager import ConnectionManager

redis_config = {
    "url": f"redis://{config('REDIS_HOST')}",
    "decode_responses": True,
    "encoding": "utf-8",
}

domain = config("DOMAIN")

manager = ConnectionManager()
