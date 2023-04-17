from PyQt5.QtWidgets import QWidget, QSplitter
from PyQt5.QtCore import Qt

from ..widgets import VLayout, HLayout, Frame
from .left_menu import LeftMenu
from .right_pages import RightPages
from .central_pages import CentralPages
from .panel import Panel


class MainView(QWidget):
    def __init__(self, parent: QWidget):
        super().__init__(parent=parent)
        self.setObjectName(self.__class__.__name__)

    def init(self) -> 'MainView':
        layout = VLayout().init()
        layout.addWidget(Panel(self).init(), alignment=Qt.AlignTop)

        splitter = QSplitter(self)
        splitter.addWidget(LeftMenu(self, splitter, 300).init())
        splitter.addWidget(CentralPages(self).init())
        splitter.addWidget(RightPages(self, splitter, 400).init())

        # frame = Frame(self, 'MainViewFrame')
        # vbox = VLayout()
        # vbox.addWidget(splitter)
        layout.addWidget(splitter)
        self.setLayout(layout)

        return self
