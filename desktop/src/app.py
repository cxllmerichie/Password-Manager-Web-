from aioqui.widgets import Window
from aioqui import CONTEXT
from aioqui.asynq import asyncSlot


class App(Window):
    # all imports must be placed only in the class, otherwise `-1073740791 (0xC0000409)`
    # issue: while running (init load) it sees the import and usage from Qt in `assets`, and Qt itself conflicts
    # with main created thread in `main.py` creating more threads in `assets`

    def __init__(self):
        from . import qss

        super().__init__(self.__class__.__name__, qss=(
            qss.status_bar.css,
            qss.app.css,
            qss.components.popup,  # non-obvious css, since all popups parent is `popup_layout_widget.core` == `self`
        ))

    async def init(self) -> 'App':
        from .misc import SIZES

        self.resize(SIZES.App)
        if not CONTEXT['storage']:
            from .components import IntroPopup

            await IntroPopup(self).display()
        else:
            from .misc.const import db, tables
            from .views.central_widget import CentralWidget
            from .components import StatusBar, Panel

            assert await db.create_pool()
            await db.execute(tables)

            self.setPanel(await Panel(self).init())
            self.setCentralWidget(await CentralWidget(self).init())
            self.setStatusBar(await StatusBar(self).init())
        return self

    @asyncSlot()
    async def close(self):
        from .misc.const import db

        assert await db.close_pool()
        return super().close()
