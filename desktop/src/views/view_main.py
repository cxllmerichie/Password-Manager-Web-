from aioqui.widgets import Splitter, Parent
from aioqui import CONTEXT

from .menu_left import LeftMenu
from .menu_right import RightPages
from .menu_central import CentralItems
from .. import qss


class MainView(Splitter):
    def __init__(self, parent: Parent):
        super().__init__(parent, self.__class__.__name__, qss=qss.view_main.css)

    async def init(self) -> 'MainView':
        await super().init(
            items=[
                await LeftMenu(self).init(),
                await CentralItems(self).init(),
                await RightPages(self).init()
            ]
        )
        await CONTEXT.RightPagesCategory.show_create()
        CONTEXT.LeftMenu.expand()
        return self
