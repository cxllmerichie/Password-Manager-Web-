from PyQt5.QtWidgets import QWidget, QStackedWidget, QFrame, QScrollArea
from PyQt5.QtCore import Qt, pyqtSlot
from typing import Any

from ..widgets import Label, Layout, ScrollArea, Button, SideMenu
from ..misc import Icons, Sizes, api
from .countable_button import CountableButton
from .items import CentralItem
from .. import css


class LeftMenu(SideMenu, QWidget):
    def __init__(self, parent: QWidget, width: int):
        QWidget.__init__(self, parent)
        SideMenu.__init__(self, parent, self.__class__.__name__, True, width, Qt.Horizontal)
        self.setStyleSheet(css.left_menu.css + css.components.scroll)
        self.setAttribute(Qt.WA_StyledBackground, True)

    def init(self) -> 'LeftMenu':
        categories = api.categories()
        layout = Layout.vertical().init(
            spacing=5, margins=(10, 10, 0, 0), alignment=Qt.AlignTop,
            items=[
                Label(self, 'LeftMenuItemsLabel').init(
                    text='Items'
                ), Qt.AlignVCenter,
                CountableButton(self).init(
                    icon=Icons.HOME, text='All items', total=sum([len(category['items']) for category in categories])
                ), Qt.AlignLeft,
                CountableButton(self).init(
                    icon=Icons.STAR.adjusted(size=Icons.HOME.size), text='Favourite',
                    total=sum(
                        [len([1 for item in category['items'] if item['is_favourite']]) for category in categories])
                ), Qt.AlignLeft,
                Button(self, 'AddCategoryBtn').init(
                    text='Category', icon=Icons.PLUS, slot=self.add_category
                ),
                Label(self, 'LeftMenuCategoriesLabel').init(
                    text='Categories'
                )
            ]
        )
        if not len(categories):
            layout.addWidget(Label(self, 'NoCategoriesLbl').init(
                text='You don\'t have any categories yet', alignment=Qt.AlignVCenter | Qt.AlignHCenter,
                wrap=True
            ), alignment=Layout.Center)
        else:
            layout.addWidget(ScrollArea(self, 'CategoriesScrollArea').init(
                horizontal=False, vertical=True, orientation=Layout.Vertical, alignment=Layout.Top, spacing=5,
                items=[
                    CountableButton(self).init(
                        icon=Icons.from_bytes(category['icon']).adjusted(size=Icons.HOME.size), text=category['title'],
                        total=len(category['items']), slot=lambda checked, c=category: self.show_category(c)
                    ) for category in categories
                ]
            ))
        self.setLayout(layout)
        return self

    def show_category(self, category: dict[str, Any]):
        central_pages = self.parent().parent().findChild(QStackedWidget, 'CentralPages')
        central_pages.setCurrentIndex(0)
        items = central_pages.currentWidget()
        layout = items.ItemsScrollArea.widget().layout()
        layout.clear()
        for item in category['items']:
            layout.addWidget(CentralItem(items, item, self.show_item).init())

        right_pages = self.parent().parent().findChild(QStackedWidget, 'RightPages')
        right_pages.setCurrentIndex(0)
        right_pages.currentWidget().show_category(category)
        right_pages.expand()

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
