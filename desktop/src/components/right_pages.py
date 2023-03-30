from PyQt5.QtWidgets import QStackedWidget, QWidget
from PyQt5.QtCore import Qt

from ..css import right_pages


class RightPages(QStackedWidget):
    def __init__(self, parent: QWidget, width: int):
        super().__init__(parent)
        self.setObjectName(self.__class__.__name__)
        self.setStyleSheet(right_pages.css)
        self._width = width

    async def init(self) -> 'RightPages':
        return self

    async def expand(self):
        self.setFixedWidth(self._width)

    async def shrink(self):
        self.setFixedWidth(0)
