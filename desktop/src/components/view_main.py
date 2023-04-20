from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt

from ..widgets import Layout, Frame, Widget, Splitter
from .left_menu import LeftMenu
from .right_pages import RightPages
from .central_pages import CentralPages
from .panel import Panel
from .. import css


class MainView(Widget):
    def __init__(self, parent: QWidget):
        super().__init__(parent, self.__class__.__name__,
                         stylesheet=css.components.splitter)

    def init(self) -> 'MainView':
        frame = Frame(self, 'MainViewFrame')
        splitter = Splitter(frame, 'MainViewSplitter').init(items=[
            CentralPages(self).init(),
            RightPages(self, 300).init()
        ])
        self.setLayout(Layout.vertical().init(
            items=[
                Panel(self).init(), Qt.AlignTop,
                frame.init(
                    layout=Layout.horizontal().init(
                        items=[
                            LeftMenu(self, 220).init(),
                            splitter
                        ]
                    )
                )
            ]
        ))
        self.LeftMenu.expand()
        self.RightPages.shrink()
        return self
