from typing import Literal
from .logging import logger

def print(msg: str, args=None, exc_info=None, logging_level: Literal[50, 40, 30, 20, 10] = 20):
    logger._log(logging_level, msg, args=args, exc_info=exc_info, stacklevel=2)
