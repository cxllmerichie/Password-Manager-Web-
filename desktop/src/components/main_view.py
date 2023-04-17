from PyQt5.QtWidgets import QWidget, QSplitter
from PyQt5.QtCore import Qt

from ..widgets import Layout, Frame
from .left_menu import LeftMenu
from .right_pages import RightPages
from .central_pages import CentralPages
from .panel import Panel


class MainView(QWidget):
    def __init__(self, parent: QWidget):
        super().__init__(parent=parent)
        self.setObjectName(self.__class__.__name__)

    def init(self) -> 'MainView':
        layout = Layout.vertical().init()
        layout.addWidget(Panel(self).init(), alignment=Qt.AlignTop)

        frame = Frame(self, 'MainViewFrame')
        splitter = QSplitter(frame)
        splitter.addWidget(CentralPages(self).init())
        splitter.addWidget(RightPages(self, splitter, 300).init())

        hbox = Layout.horizontal(frame).init()
        hbox.addWidget(left_menu := LeftMenu(self, 220).init())
        hbox.addWidget(splitter)

        layout.addWidget(frame.init(layout=hbox))
        self.setLayout(layout)

        left_menu.shrink()
        return self
