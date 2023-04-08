from PyQt5.QtWidgets import QStackedWidget

from ..css import central_pages
from .items import Items


class CentralPages(QStackedWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.setObjectName(self.__class__.__name__)
        self.setStyleSheet(central_pages.css)

    def init(self) -> 'CentralPages':
        self.addWidget(Items(self).init(items=[]))
        self.setCurrentIndex(0)
        return self
