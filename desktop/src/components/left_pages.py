from PyQt5.QtWidgets import QStackedWidget, QWidget
from PyQt5.QtCore import Qt

from ..widgets import SideMenu
from ..css import left_pages


class LeftPages(SideMenu):
    def __init__(self, parent: QWidget, width: int):
        super().__init__(parent, width)
        self.setObjectName(self.__class__.__name__)
        self.setStyleSheet(left_pages.css)

    async def init(self) -> 'LeftPages':
        return self
