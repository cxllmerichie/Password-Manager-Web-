from PyQt5.QtWidgets import QWidget, QSplitter

from .rp_category import RP_Category
from .rp_item import RP_Item
from ..widgets import SplitterWidgetExt, StackedWidget
from .. import css


class RightPages(SplitterWidgetExt, StackedWidget):
    def __init__(self, parent: QWidget, splitter: QSplitter, width: int):
        super().__init__(parent, self.__class__.__name__)
        self.setStyleSheet(css.menu_right_pages.css)

        self.expand_to = width
        self.splitter = splitter

    def init(self) -> 'RightPages':
        self.addWidget(RP_Category(self).init())
        self.addWidget(RP_Item(self).init())
        return self
