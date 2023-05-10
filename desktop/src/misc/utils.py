from datetime import datetime
import os

from .assets import EXTENSIONS


class Storage:
    LOCAL = 'local'
    REMOTE = 'remote'
    HYBRID = 'hybrid'


def icon_name() -> str:
    return f"{datetime.now().strftime('%d.%m.%Y %H-%M-%S')}.{EXTENSIONS.ICON}"


def icon_path() -> str:
    return os.path.join(os.path.abspath('icons'), icon_name())


def save_icon(icon: bytes | str) -> None:
    with open(icon_path(), 'wb') as file:
        file.write(eval(icon))
