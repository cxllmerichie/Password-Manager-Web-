from typing import Any, Coroutine
from datetime import datetime
from enum import Enum
import asyncio
import socket
import os

from .assets import EXTENSIONS



class Storage(Enum):
    LOCAL = 'local'
    REMOTE = 'remote'
    HYBRID = 'hybrid'


def prepare(coroutine: Coroutine) -> Any:
    # return asyncio.get_event_loop().run_until_complete(coroutine)
    from qcontextapi import qasync
    return asyncio.get_event_loop().run_until_complete(coroutine)


def is_connected():
    try:
        socket.create_connection(('8.8.8.8', 53))
        return True
    except OSError:
        pass
    return False


def icon_name() -> str:
    return f"{datetime.now().strftime('%d.%m.%Y %H-%M-%S')}.{EXTENSIONS.ICON}"


def icon_path() -> str:
    return os.path.join(os.path.abspath('icons'), icon_name())


def save_icon(icon: bytes | str) -> None:
    with open(icon_path(), 'wb') as file:
        file.write(eval(icon))
