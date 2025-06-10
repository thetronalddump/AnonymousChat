import logging
from dataclasses import dataclass
from typing import Final

from config import redis_config
from src.database.cache import RoomsControl


@dataclass(frozen=True)
class LoggerHandlers:
    file_handler: Final[logging.FileHandler] = logging.FileHandler("./logs/service.log")
    console_handler: Final[logging.StreamHandler] = logging.StreamHandler()


@dataclass(frozen=True)
class DBEntities:
    rooms_control: Final[RoomsControl] = RoomsControl(redis_config)