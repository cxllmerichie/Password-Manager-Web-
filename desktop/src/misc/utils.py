from typing import Any, Optional, Iterable
from aioqui import CONTEXT


async def find(
        where: list[dict[str, Any]],
        key: Any,
        value: Any
) -> tuple[Optional[int], Optional[dict[str, Any]]]:
    for index, item in enumerate(where):
        if item.get(key) == value:
            return index, item
    return None, None


async def serializable(dictionary: dict[str, Any], exceptions: Iterable[str] = ()) -> dict[str, Any]:
    def validate(value: Any):
        if isinstance(value, bool):
            return True
        elif value is None:
            return False
        elif isinstance(value, str):
            return len(value)

    return {key: value for key, value in dictionary.items() if validate(value) or key in exceptions}


def auth_h() -> dict[str, Any]:
    return accept_h() | {'Authorization': f"Bearer {CONTEXT['token']}"}


def accept_h() -> dict[str, Any]:
    return {'accept': 'application/json'}


def content_h() -> dict[str, Any]:
    return {'Content-Type': 'application/json'}


def login_h() -> dict[str, Any]:
    return accept_h() | {'Content-Type': 'application/x-www-form-urlencoded'}


def accept_content_h():
    return accept_h() | content_h()


class Storage:
    LOCAL = 'local'
    REMOTE = 'remote'
    HYBRID = 'hybrid'

    @staticmethod
    def local():
        return CONTEXT['storage'] == Storage.LOCAL

    @staticmethod
    def remote():
        return CONTEXT['storage'] == Storage.REMOTE
