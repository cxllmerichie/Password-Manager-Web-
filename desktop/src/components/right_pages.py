from PyQt5.QtWidgets import QWidget

from .rp_category import RP_Category
from .rp_item import RP_Item
from ..widgets import SplitterWidgetExt, StackedWidget
from .. import css


class RightPages(SplitterWidgetExt, StackedWidget):
    def __init__(self, parent: QWidget, width: int):
        StackedWidget.__init__(self, parent, self.__class__.__name__,
                               stylesheet=css.right_pages.css)
        SplitterWidgetExt.__init__(self, width)

    def init(self) -> 'RightPages':
        self.addWidget(RP_Category(self).init())
        self.addWidget(RP_Item(self).init())
        return self
