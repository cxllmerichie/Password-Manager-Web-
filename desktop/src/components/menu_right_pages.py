from PyQt5.QtWidgets import QWidget, QSplitter

from .rp_category import Category
from .rp_item import Item
from ..widgets import SplitterWidgetExtension, StackedWidget
from .. import css


class RightPages(SplitterWidgetExtension, StackedWidget):
    def __init__(self, parent: QWidget, splitter: QSplitter, width: int):
        super().__init__(parent, self.__class__.__name__)
        self.setStyleSheet(css.menu_right_pages.css)

        self.expand_to = width
        self.splitter = splitter

    def init(self) -> 'RightPages':
        self.addWidget(Category(self).init())
        self.addWidget(Item(self).init())
        return self
