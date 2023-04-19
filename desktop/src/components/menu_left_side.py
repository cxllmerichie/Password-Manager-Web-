from PyQt5.QtWidgets import QWidget, QStackedWidget, QFrame
from PyQt5.QtCore import Qt, pyqtSlot
from typing import Any

from ..widgets import Label, Layout, ScrollArea, Button, SideMenu, Widget
from ..misc import Icons, api, Icon
from .. import css


class CountableButton(Button):
    def __init__(self, parent: QWidget):
        super().__init__(parent, self.__class__.__name__)

    def init(
            self, *,
            icon: Icon, text: str, total: int,
            alignment: Qt.Alignment = None, slot: callable = lambda: None
    ) -> 'CountableButton':
        self.setLayout(Layout.horizontal().init(
            margins=(10, 0, 0, 0), spacing=10, alignment=Qt.AlignLeft,
            items=[
                Button(self, 'CountableButtonIcon').init(
                    size=icon.size, icon=icon, disabled=True
                ),
                Label(self, 'CountableButtonLbl').init(
                    text=text, alignment=alignment, elided=True
                ),
                Label(self, 'CountableButtonCountLbl').init(
                    text=str(total)
                ), Qt.AlignRight
            ]
        ))
        self.clicked.connect(slot)
        return self


class LeftMenu(SideMenu, Widget):
    def __init__(self, parent: QWidget, width: int):
        Widget.__init__(self, parent, self.__class__.__name__, stylesheet=css.menu_left_side.css + css.components.scroll)
        SideMenu.__init__(self, width, Qt.Horizontal)

    def init(self) -> 'LeftMenu':
        categories = api.categories()
        self.setLayout(Layout.vertical().init(
            spacing=5, margins=(10, 10, 0, 0), alignment=Qt.AlignTop,
            items=[
                Label(self, 'LeftMenuItemsLabel').init(
                    text='Items'
                ), Qt.AlignVCenter,
                AllItemsBtn := CountableButton(self).init(
                    icon=Icons.HOME, text='All items', total=0
                ), Qt.AlignLeft,
                FavItemsBtn := CountableButton(self).init(
                    icon=Icons.STAR.adjusted(size=Icons.HOME.size), text='Favourite',
                    total=sum([len([1 for item in category['items'] if item['is_favourite']]) for category in categories])
                ), Qt.AlignLeft,
                Button(self, 'AddCategoryBtn').init(
                    text='Category', icon=Icons.PLUS, slot=self.add_category
                ),
                Label(self, 'LeftMenuCategoriesLabel').init(
                    text='Categories'
                ),
                Label(self, 'NoCategoriesLbl', False).init(
                    text='You don\'t have any categories yet', alignment=Qt.AlignVCenter | Qt.AlignHCenter,
                    wrap=True
                ), Layout.Center,
                ScrollArea(self, 'CategoriesScrollArea', False).init(
                    horizontal=False, vertical=True, orientation=Layout.Vertical, alignment=Layout.Top, spacing=5
                )
            ]
        ))
        self.AllItemsBtn = AllItemsBtn
        self.FavItemsBtn = FavItemsBtn
        self.show_categories(categories)
        return self

    def show_categories(self, categories: list[dict[str, Any]]):
        if not len(categories):
            self.CategoriesScrollArea.setVisible(False)
            return self.NoCategoriesLbl.setVisible(True)
        layout = self.CategoriesScrollArea.widget().layout()
        layout.clear()
        for category in categories:
            layout.addWidget(
                CountableButton(self).init(
                    icon=Icons.from_bytes(category['icon']).adjusted(size=Icons.HOME.size), text=category['title'],
                    total=len(category['items']), slot=lambda checked, _category=category: self.show_category(_category)
                )
            )
        self.NoCategoriesLbl.setVisible(False)
        self.CategoriesScrollArea.setVisible(True)
        self.AllItemsBtn.CountableButtonCountLbl.setText(str(sum([len(category['items']) for category in categories])))
        self.FavItemsBtn.CountableButtonCountLbl.setText(str(sum([len([1 for item in category['items'] if item['is_favourite']]) for category in categories])))

    def show_category(self, category: dict[str, Any]):
        MainView = self.parent().parent()
        RightPages = MainView.RightPages
        Category = RightPages.findChild(QFrame, 'Category')
        Category.show_category(category)
        RightPages.setCurrentWidget(Category)
        RightPages.expand()
        #
        # # expand right pages
        # RightPages = self.parent()
        # Category = RightPages.findChild(QWidget, 'Category')
        # RightPages.setCurrentWidget(Category)
        # # display items in main view
        # CentralPages = self.parent().parent().parent().parent().findChild(QStackedWidget, 'CentralPages')
        # CentralPages.setCurrentWidget(CentralPagesItems := CentralPages.CentralPagesItems)
        #
        # Item = RightPages.findChild(QWidget, 'Item')
        # layout = CentralPagesItems.ItemsScrollArea.widget().layout()
        # layout.clear()
        # for item in category['items']:
        #     print(item)
        #     layout.addWidget(CentralPagesItem(CentralPagesItems, item, Item.show_item).init())
        #
        # RightPages = self.parent().parent().findChild(QStackedWidget, 'RightPages').findChild(QFrame, 'Category')
        # Category = RightPages
        # Category.show_category(category)
        ...

    def show_item(self, item: dict[str, Any]):
        right_pages = self.parent().parent().findChild(QStackedWidget, 'RightPages')
        right_pages.setCurrentIndex(1)
        right_pages.currentWidget().show_item(item)
        right_pages.expand()

    @pyqtSlot()
    def add_category(self):
        right_pages = self.parent().parent().findChild(QStackedWidget, 'RightPages')
        right_pages.findChild(QFrame, 'Category').show_create_category()
        right_pages.setCurrentIndex(0)
        right_pages.expand()
