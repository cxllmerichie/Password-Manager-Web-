from qcontextapi.widgets import StackedWidget, Layout
from qcontextapi.extensions import SplitterWidgetExt
from PyQt5.QtWidgets import QWidget

from .right_pages_category import RightPagesCategory
from .right_pages_item import RightPagesItem
from ..misc import SIZES
from .. import css


class RightPages(SplitterWidgetExt, StackedWidget):
    def __init__(self, parent: QWidget):
        StackedWidget.__init__(self, parent, self.__class__.__name__, stylesheet=css.right_pages.css)
        SplitterWidgetExt.__init__(self, 300, expand_max=SIZES.RightMenu.w, orientation=Layout.Horizontal)

    def init(self) -> 'RightPages':
        self.addWidget(RightPagesCategory(self).init())
        self.addWidget(RightPagesItem(self).init())
        return self
