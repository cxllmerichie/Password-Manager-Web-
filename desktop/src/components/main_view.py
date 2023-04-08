from PyQt5.QtWidgets import QWidget
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
        vbox = VLayout().init()
        vbox.addWidget(Panel(self).init(), alignment=Qt.AlignTop)

        hbox = HLayout(self).init()
        hbox.addWidget(LeftMenu(self, 220).init())
        hbox.addWidget(CentralPages(self).init())
        hbox.addWidget(RightPages(self, 350).init())

        vbox.addWidget(Frame(self, 'MainViewFrame').init(layout=hbox))
        self.setLayout(vbox)
        return self
