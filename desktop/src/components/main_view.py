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

    async def init(self) -> 'MainView':
        vbox = await VLayout().init()
        vbox.addWidget(await Panel(self).init(), alignment=Qt.AlignTop)

        hbox = await HLayout(self).init()
        hbox.addWidget(await LeftMenu(self, 220).init())
        hbox.addWidget(await CentralPages(self).init())
        hbox.addWidget(await RightPages(self, 350).init())

        vbox.addWidget(await Frame(self, 'MainViewFrame').init(layout=hbox))
        self.setLayout(vbox)
        return self
