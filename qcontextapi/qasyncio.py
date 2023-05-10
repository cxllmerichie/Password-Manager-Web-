from typing import Coroutine, Callable
from loguru import logger
import asyncio


class QAsync:
    aiobject_t = type[Callable | Coroutine]
    aiobjects: list[aiobject_t] = []
    is_handling: bool = False

    def __call__(self, aiobject: aiobject_t) -> None:
        if not self.is_handling:
            logger.warning('`QAsync.handle()` was not called before using `QAsync`')
        self.aiobjects.append(aiobject)

    def handle(self):
        async def handler():
            while True:
                for aiobject in self.aiobjects:
                    print(f'{await aiobject=}')
                    self.aiobjects.remove(aiobject)
                await asyncio.sleep(.5)

        if not self.is_handling:
            asyncio.get_event_loop().create_task(handler())
            self.is_handling = True
        else:
            logger.warning('`QAsync.handler` already running')


qasync = QAsync()

# will never work
