from aioqui.widgets import StackedWidget, Parent
from aioqui.widgets.extensions import SplitterWidgetExt

from .rp_category import RightPagesCategory
from .rp_item import RightPagesItem
from ..misc import SIZES
from .. import qss


class RightPages(SplitterWidgetExt, StackedWidget):
    def __init__(self, parent: Parent):
        StackedWidget.__init__(self, parent, self.__class__.__name__, qss=qss.menu_right.css)
        SplitterWidgetExt.__init__(self, SIZES.RightMenuFix, SIZES.RightMenuMin, SIZES.RightMenuMax)

    async def init(self) -> 'RightPages':
        await super().init(
            items=[
                await RightPagesCategory(self).init(

                ),
                await RightPagesItem(self).init(

                )
            ]
        )
        return self
