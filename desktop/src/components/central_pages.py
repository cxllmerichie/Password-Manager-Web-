from PyQt5.QtWidgets import QStackedWidget

from .items import Items
from .. import css


class CentralPages(QStackedWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.setObjectName(self.__class__.__name__)
        self.setStyleSheet(css.central_pages.css)

    def init(self) -> 'CentralPages':
        self.addWidget(Items(self).init())
        self.setCurrentIndex(0)
        return self
