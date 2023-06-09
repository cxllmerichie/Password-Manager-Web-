from aioqui.widgets import Splitter, Parent
from aioqui import CONTEXT

from .left_menu import LeftMenu
from .right_pages import RightPages
from .central_items import CentralItems
from .. import qss


class MainView(Splitter):
    def __init__(self, parent: Parent):
        super().__init__(parent, self.__class__.__name__, qss=qss.view_main.css)

    async def init(self) -> 'MainView':
        central_items = await CentralItems(self).init()
        right_pages = await RightPages(self).init()
        left_menu = await LeftMenu(self).init()
        await super().init(
            items=[
                left_menu,
                central_items,
                right_pages
            ]
        )
        await CONTEXT.RightPagesCategory.show_create()
        left_menu.expand()
        right_pages.shrink()
        return self
