from aioqui.widgets import Window
from aioqui import CONTEXT
from aioqui.asynq import asyncSlot


class App(Window):
    # all imports must be placed only in the class, otherwise `Process finished with exit code -1073740791 (0xC0000409)`
    # issue: while running (init load) it sees the import and usage from PyQt5 in `assets`, and PyQt5 itself conflicts
    # with main created thread in `main.py` creating more threads in `assets`

    def __init__(self):
        from . import qss

        super().__init__(self.__class__.__name__, qss=(qss.status_bar.css, qss.app.css))

    async def init(self) -> 'App':
        from .misc import SIZES

        self.resize(SIZES.App)
        if not CONTEXT['storage']:
            from .components import IntroPopup

            _ = await IntroPopup(self).init()
        else:
            from .misc.const import db, tables
            from .views.central_widget import CentralWidget
            from .components import StatusBar, Panel

            assert await db.create_pool()
            await db.execute(tables)
            statusbar = await StatusBar(self).init()
            self.setPanel(await Panel(self).init())
            self.setCentralWidget(await CentralWidget(self).init())
            self.setStatusBar(statusbar)
            await statusbar.post_init()
        return self

    @asyncSlot()
    async def close(self) -> bool:
        from .misc.const import db

        assert await db.close_pool()
        return super().close()
