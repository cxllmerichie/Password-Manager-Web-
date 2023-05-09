from qcontextapi.widgets import Layout, Widget, Splitter
from qcontextapi import CONTEXT
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt

from .left_menu import LeftMenu
from .right_pages import RightPages
from .central_items import CentralItems
from ..components import Panel
from .. import stylesheets


class MainView(Widget):
    def __init__(self, parent: QWidget):
        super().__init__(parent, self.__class__.__name__, stylesheet=stylesheets.view_main.css)

    def init(self) -> 'MainView':
        central_items = CentralItems(self).init()
        right_pages = RightPages(self).init()
        left_menu = LeftMenu(self).init()

        splitter = Splitter(self, 'MainViewSplitter').init()
        splitter.addWidget(left_menu)
        splitter.addWidget(central_items, False)
        splitter.addWidget(right_pages)

        self.setLayout(Layout.vertical().init(
            items=[
                Panel(self).init(), Qt.AlignTop,
                splitter
            ]
        ))
        CONTEXT.RightPagesCategory.show_create()
        right_pages.shrink()
        left_menu.expand()
        return self
