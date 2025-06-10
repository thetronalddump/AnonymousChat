from decouple import config


redis_config = {
    "url": f"redis://{config('REDIS_HOST')}",
    "decode_responses": True,
    "encoding": "utf-8"
}
