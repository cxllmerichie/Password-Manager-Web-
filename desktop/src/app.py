from aioqui.widgets import Window
from aioqui import CONTEXT
from aioqui.qasyncio import asyncSlot


class App(Window):
    # all imports must be placed only in the class, otherwise `Process finished with exit code -1073740791 (0xC0000409)`
    # issue: while running (init load) it sees the import and usage from PyQt5 in `assets`, and PyQt5 itself conflicts
    # with main created thread in `main.py` creating more threads in `assets`

    def __init__(self):
        from . import stylesheets

        super().__init__(self.__class__.__name__, stylesheet=stylesheets.status_bar.css +
                                                             stylesheets.app.css)

    async def init(self) -> 'App':
        from .misc import SIZES
        from .misc.const import db, tables

        assert await db.create_pool()
        await db.execute(tables)

        self.resize(SIZES.App)
        self.setWindowFlag(Window.Frameless)
        if not CONTEXT['storage']:
            from .components import IntroPopup

            _ = await IntroPopup(self).init()
        else:
            from .views.central_widget import CentralWidget
            from .components import StatusBar

            statusbar = await StatusBar(self).init()
            self.setCentralWidget(await CentralWidget(self).init())
            self.setStatusBar(statusbar)
            await statusbar.post_init()
        return self

    @asyncSlot()
    async def close(self) -> bool:
        from .misc.const import db

        assert await db.close_pool()
        return super().close()
