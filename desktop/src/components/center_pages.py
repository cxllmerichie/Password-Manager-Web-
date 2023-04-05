from PyQt5.QtWidgets import QStackedWidget
from PyQt5.QtCore import Qt

from ..css import center_pages
from .items import Items


class CenterPages(QStackedWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.setObjectName(self.__class__.__name__)
        self.setStyleSheet(center_pages.css)

    async def init(self) -> 'CenterPages':
        return self
