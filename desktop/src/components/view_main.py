from PyQt5.QtWidgets import QWidget, QSplitter
from PyQt5.QtCore import Qt

from ..widgets import Layout, Frame, Widget
from .left_menu import LeftMenu
from .right_pages import RightPages
from .central_pages import CentralPages
from .panel import Panel


class MainView(Widget):
    def __init__(self, parent: QWidget):
        super().__init__(parent, self.__class__.__name__)

    def init(self) -> 'MainView':
        frame = Frame(self, 'MainViewFrame')

        splitter = QSplitter(frame)
        splitter.addWidget(CentralPages(self).init())
        splitter.addWidget(right_pages := RightPages(self, splitter, 300).init())

        self.setLayout(Layout.vertical().init(
            items=[
                Panel(self).init(), Qt.AlignTop,
                frame.init(
                    layout=Layout.horizontal().init(
                        items=[
                            left_menu := LeftMenu(self, 220).init(),
                            splitter
                        ]
                    )
                )
            ]
        ))
        left_menu.expand()
        right_pages.shrink()
        return self
