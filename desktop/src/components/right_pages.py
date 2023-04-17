from PyQt5.QtWidgets import QStackedWidget, QWidget, QSplitter

from .category import Category
from .item import Item
from ..widgets import SplitterWidget
from .. import css


class RightPages(QStackedWidget, SplitterWidget):
    def __init__(self, parent: QWidget, splitter: QSplitter, width: int):
        super().__init__(parent)
        self.setObjectName(self.__class__.__name__)
        self.setStyleSheet(css.right_pages.css)

        self.expand_to = width
        self.splitter = splitter

    def init(self) -> 'RightPages':
        self.addWidget(Category(self).init())
        self.addWidget(Item(self).init())
        return self
