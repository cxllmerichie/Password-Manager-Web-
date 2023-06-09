from aioqui.widgets import StackedWidget, Parent
from aioqui.widgets.extensions import SplitterWidgetExt

from .right_pages_category import RightPagesCategory
from .right_pages_item import RightPagesItem
from ..misc import SIZES
from .. import qss


class RightPages(SplitterWidgetExt, StackedWidget):
    def __init__(self, parent: Parent):
        StackedWidget.__init__(self, parent, self.__class__.__name__, qss=qss.right_pages.css)
        SplitterWidgetExt.__init__(self, expand_to=SIZES.RightMenuDefault.w, expand_max=SIZES.RightMenuMax.w, expand_min=SIZES.RightMenuMin.w)

    async def init(self) -> 'RightPages':
        await super().init(
            items=[
                await RightPagesCategory(self).init(),
                await RightPagesItem(self).init()
            ]
        )
        return self
