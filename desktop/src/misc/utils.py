from typing import Any, Iterable
from aioqui import CONTEXT


async def prepare(data: dict[str, Any], exceptions: Iterable[str] = ()) -> dict[str, Any]:
    final = {}
    for key, value in data.items():
        if key in exceptions:
            final[key] = value
            continue
        if isinstance(value, str) and not len(value):
            continue
        elif isinstance(value, bytes) and value == b'':
            continue
        final[key] = value
    return final


def auth_h() -> dict[str, Any]:
    return accept_h() | {'Authorization': f"Bearer {CONTEXT['token']}"}


def accept_h() -> dict[str, Any]:
    return {'accept': 'application/json'}


def content_h() -> dict[str, Any]:
    return {'Content-Type': 'application/json'}


def login_h() -> dict[str, Any]:
    return accept_h() | {'Content-Type': 'application/x-www-form-urlencoded'}


def accept_content_h() -> dict[str, Any]:
    return accept_h() | content_h()


class Storage:
    LOCAL = 'local'
    REMOTE = 'remote'

    @staticmethod
    def is_local():
        return CONTEXT['storage'] == Storage.LOCAL

    @staticmethod
    def is_remote():
        return CONTEXT['storage'] == Storage.REMOTE
