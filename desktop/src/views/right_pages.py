from qcontextapi.widgets import StackedWidget, Layout
from qcontextapi.extensions import SplitterWidgetExt
from PyQt5.QtWidgets import QWidget

from .right_pages_category import RightPagesCategory
from .right_pages_item import RightPagesItem
from ..misc import SIZES
from .. import stylesheets


class RightPages(SplitterWidgetExt, StackedWidget):
    def __init__(self, parent: QWidget):
        StackedWidget.__init__(self, parent, self.__class__.__name__, stylesheet=stylesheets.right_pages.css)
        SplitterWidgetExt.__init__(self, SIZES.RightMenuDefault.w,
                                   expand_max=SIZES.RightMenuMax.w, expand_min=SIZES.RightMenuMin.w,
                                   orientation=Layout.Horizontal)

    async def init(self) -> 'RightPages':
        self.addWidget(await RightPagesCategory(self).init())
        self.addWidget(await RightPagesItem(self).init())
        return self
