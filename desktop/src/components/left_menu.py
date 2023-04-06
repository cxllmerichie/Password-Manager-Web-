from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt

from ..css import left_menu
from ..widgets import Label, VLayout, SideMenu, ScrollArea
from ..misc import Icons, Sizes, API
from ..components.countable_button import CountableButton


class LeftMenu(QWidget, SideMenu):
    def __init__(self, parent: QWidget, width: int):
        super(QWidget, self).__init__(parent)
        self.setObjectName(self.__class__.__name__)
        self.setStyleSheet(left_menu.css)
        self.setAttribute(Qt.WA_StyledBackground, True)

        self.expand_to = width

    async def __layout(self) -> VLayout:
        vlayout = await VLayout().init(spacing=5, margins=(10, 10, 0, 0), alignment=Qt.AlignTop)
        vlayout.addWidget(await Label(self, 'LeftMenuItemsLabel').init(
            text='Items'
        ), alignment=Qt.AlignVCenter)
        vlayout.addWidget(await CountableButton(self).init(
            icon=Icons.HOME, text='All items', total=0
        ), alignment=Qt.AlignLeft)
        vlayout.addWidget(await CountableButton(self).init(
            icon=Icons.FAVOURITE, text='Favourites', total=0
        ), alignment=Qt.AlignLeft)
        vlayout.addWidget(await Label(self, 'LeftMenuCategoriesLabel').init(
            text='Categories'
        ))
        categories = API.categories(self.app.settings.value('token'))
        if not len(categories):
            vlayout.addWidget(await Label(self, 'NoCategoriesLbl').init(
                text='You don\'t have any categories yet', alignment=Qt.AlignVCenter | Qt.AlignHCenter,
                wrap=True, size=Sizes.NoCategoriesLbl
            ), alignment=VLayout.CenterCenter)
        else:
            items = [await CountableButton(self).init(icon=Icons.FAVOURITE, text=c, total=0) for c in categories]
            sarea = await ScrollArea(self, 'CategoriesScrollArea').init(items=items)
            sarea.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
            vlayout.addWidget(sarea)
        return vlayout

    @property
    def app(self):
        return self.parent().parent().parent()

    async def init(self) -> 'LeftMenu':
        self.setLayout(await self.__layout())
        self.shrink()
        return self
