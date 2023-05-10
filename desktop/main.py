from PyQt5.QtWidgets import QApplication
import functools
import asyncio
import qasync
import sys

from src import App


async def main():
    def close_future(future, loop):
        loop.call_later(10, future.cancel)
        future.cancel()

    loop = asyncio.get_event_loop()
    future = asyncio.Future()

    app = QApplication.instance()
    if hasattr(app, "aboutToQuit"):
        getattr(app, "aboutToQuit").connect(
            functools.partial(close_future, future, loop)
        )

    # from qcontextapi import CONTEXT
    # CONTEXT['storage'] = None
    # CONTEXT['token'] = None
    qapp = QApplication(sys.argv)
    qapp.setStyle('Windows')
    App().init().show()

    await future
    return True


if __name__ == "__main__":
    try:
        qasync.run(main())
    except asyncio.exceptions.CancelledError:
        sys.exit(0)


# ToDo: add password generating procedure (fetch from api)
# ToDo: create "Loader" using threads while waiting for displaying items in CentralPagesItems
# ToDo: multilang (translations)
