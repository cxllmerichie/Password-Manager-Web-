from PyQt5.QtWidgets import QWidget, QStackedWidget
from PyQt5.QtCore import Qt

from ..css import left_menu
from ..widgets import Label, VLayout, SideMenu, ScrollArea, Button
from ..misc import Icons, Sizes, api
from ..components.countable_button import CountableButton


class LeftMenu(QWidget, SideMenu):
    def __init__(self, parent: QWidget, width: int):
        super(QWidget, self).__init__(parent)
        self.setObjectName(self.__class__.__name__)
        self.setStyleSheet(left_menu.css)
        self.setAttribute(Qt.WA_StyledBackground, True)

        self.expand_to = width

    async def init(self) -> 'LeftMenu':
        vlayout = await VLayout().init(spacing=5, margins=(10, 10, 0, 0), alignment=Qt.AlignTop)
        vlayout.addWidget(await Label(self, 'LeftMenuItemsLabel').init(
            text='Items'
        ), alignment=Qt.AlignVCenter)
        vlayout.addWidget(await CountableButton(self).init(
            icon=Icons.HOME, text='All items', total=0
        ), alignment=Qt.AlignLeft)
        vlayout.addWidget(await CountableButton(self).init(
            icon=Icons.STAR, text='Favourite', total=0
        ), alignment=Qt.AlignLeft)
        vlayout.addWidget(await Button(self, 'AddCategoryBtn').init(
            text='Category', icon=Icons.PLUS, slot=self.add_category
        ))
        vlayout.addWidget(await Label(self, 'LeftMenuCategoriesLabel').init(
            text='Categories'
        ))
        categories = api.categories(self.app.settings.value('token'))
        if not len(categories):
            vlayout.addWidget(await Label(self, 'NoCategoriesLbl').init(
                text='You don\'t have any categories yet', alignment=Qt.AlignVCenter | Qt.AlignHCenter,
                wrap=True, size=Sizes.NoCategoriesLbl
            ), alignment=VLayout.CenterCenter)
        else:
            items = [await CountableButton(self).init(
                icon=Icons.STAR, text=c['name'], total=len(c['items']),
                slot=lambda checked, category=c: self.show_category(category)
            ) for c in categories]
            sarea = await ScrollArea(self, 'CategoriesScrollArea').init(items=items)
            sarea.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
            vlayout.addWidget(sarea)
        self.setLayout(vlayout)
        self.shrink()
        return self

    def show_category(self, category):
        right_pages = self.parent().parent().findChild(QStackedWidget, 'RightPages')
        right_pages.currentWidget().set_category(category)
        right_pages.setCurrentIndex(0)
        right_pages.expand()

    def add_category(self):
        self.parent().parent().findChild(QStackedWidget, 'RightPages').setCurrentIndex(0)
        self.parent().parent().findChild(QStackedWidget, 'RightPages').expand()

    @property
    def app(self):
        return self.parent().parent().parent()
