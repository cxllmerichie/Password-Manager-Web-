from typing import Any, Iterable
from uuid import uuid4, UUID
from threading import Thread


class ConditionalThread(Thread):
    to_complete: bool = False

    def kill(self):
        self.to_complete = False


class ConditionalThreadQueue:
    def __init__(self):
        self.__threads: dict[UUID, ConditionalThread] = {}

    def new(self, pre: callable, post: callable) -> UUID:
        if self.__threads:  # kill prev thread if exists
            key = list(self.__threads.keys())[-1]
            self.__threads[key].kill()

        def target(thread_uuid: UUID):  # create target for the new thread
            pre()
            thread = self.__threads[thread_uuid]
            if thread.to_complete:  # call post() if thread was not killed
                post()
            self.__threads.pop(thread_uuid)

        uuid = uuid4()
        thread = ConditionalThread(target=target, args=(uuid, ))
        self.__threads[uuid] = thread
        thread.start()
        return uuid

    def __getitem__(self, uuid: UUID):
        return self.__threads[uuid]


def serializable(dictionary: dict[str, Any], exceptions: Iterable[str] = ()) -> dict[str, Any]:
    def validate(value: Any):
        if isinstance(value, bool):
            return True
        elif value is None:
            return False
        elif isinstance(value, str):
            return len(value)

    return {key: value for key, value in dictionary.items() if validate(value) or key in exceptions}


def find(data: list[dict[str, Any]], key: Any, value: Any) -> tuple[int, dict[str, Any]] | None:
    for index, item in enumerate(data):
        if item.get(key) == value:
            return index, item
