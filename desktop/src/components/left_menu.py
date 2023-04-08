from PyQt5.QtWidgets import QWidget, QStackedWidget
from PyQt5.QtCore import Qt, pyqtSlot

from ..css import left_menu
from ..widgets import Label, VLayout, SideMenu, ScrollArea, Button
from ..misc import Icons, Sizes, api
from .countable_button import CountableButton


class LeftMenu(QWidget, SideMenu):
    def __init__(self, parent: QWidget, width: int):
        super(QWidget, self).__init__(parent)
        self.setObjectName(self.__class__.__name__)
        self.setStyleSheet(left_menu.css)
        self.setAttribute(Qt.WA_StyledBackground, True)

        self.expand_to = width

    def init(self) -> 'LeftMenu':
        vlayout = VLayout().init(spacing=5, margins=(10, 10, 0, 0), alignment=Qt.AlignTop)
        vlayout.addWidget(Label(self, 'LeftMenuItemsLabel').init(
            text='Items'
        ), alignment=Qt.AlignVCenter)
        vlayout.addWidget(CountableButton(self).init(
            icon=Icons.HOME, text='All items', total=0
        ), alignment=Qt.AlignLeft)
        vlayout.addWidget(CountableButton(self).init(
            icon=Icons.STAR, text='Favourite', total=0
        ), alignment=Qt.AlignLeft)
        vlayout.addWidget(Button(self, 'AddCategoryBtn').init(
            text='Category', icon=Icons.PLUS, slot=self.add_category
        ))
        vlayout.addWidget(Label(self, 'LeftMenuCategoriesLabel').init(
            text='Categories'
        ))
        if not isinstance(response := api.categories(self.app().token()), list):
            vlayout.addWidget(Label(self, 'NoCategoriesLbl').init(
                text='You don\'t have any categories yet', alignment=Qt.AlignVCenter | Qt.AlignHCenter,
                wrap=True, size=Sizes.NoCategoriesLbl
            ), alignment=VLayout.CenterCenter)
        else:
            items = [CountableButton(self).init(
                icon=Icons.STAR, text=category['title'], total=len(category['items']),
                slot=lambda checked, category=category: self.show_category(category)
            ) for category in response]
            sarea = ScrollArea(self, 'CategoriesScrollArea', False, True).init(items=items)
            vlayout.addWidget(sarea)
        self.setLayout(vlayout)
        self.shrink()
        return self

    def show_category(self, category):
        right_pages = self.parent().parent().findChild(QStackedWidget, 'RightPages')
        right_pages.currentWidget().set_category(category)
        right_pages.setCurrentIndex(0)
        right_pages.expand()

    @pyqtSlot()
    def add_category(self):
        right_pages = self.parent().parent().findChild(QStackedWidget, 'RightPages')
        right_pages.setCurrentIndex(0)
        right_pages.expand()

    def refresh(self):
        ...

    def app(self):
        return self.parent().parent().parent()
