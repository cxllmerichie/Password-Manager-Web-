from PyQt5.QtWidgets import QWidget, QStackedWidget, QFrame, QScrollArea, QSplitter
from PyQt5.QtCore import Qt, pyqtSlot
from typing import Any

from ..widgets import Label, VLayout, SplitterWidget, ScrollArea, Button
from ..misc import Icons, Sizes, api
from .countable_button import CountableButton
from .items import CentralItem
from .. import css


class LeftMenu(QWidget, SplitterWidget):
    def __init__(self, parent: QWidget, splitter: QSplitter, width: int):
        super().__init__(parent)
        self.setObjectName(self.__class__.__name__)
        self.setStyleSheet(css.left_menu.css + css.components.scroll)
        self.setAttribute(Qt.WA_StyledBackground, True)

        self.expand_to = width
        self.splitter = splitter

    def init(self) -> 'LeftMenu':
        vlayout = VLayout().init(spacing=5, margins=(10, 10, 0, 0), alignment=Qt.AlignTop)
        vlayout.addWidget(Label(self, 'LeftMenuItemsLabel').init(
            text='Items'
        ), alignment=Qt.AlignVCenter)
        categories = api.categories(self.app().token())
        vlayout.addWidget(CountableButton(self).init(
            icon=Icons.HOME, text='All items', total=sum([len(category['items']) for category in categories])
        ), alignment=Qt.AlignLeft)
        vlayout.addWidget(CountableButton(self).init(
            icon=Icons.STAR, text='Favourite',
            total=sum([len([1 for item in category['items'] if item['is_favourite']]) for category in categories])
        ), alignment=Qt.AlignLeft)
        vlayout.addWidget(Button(self, 'AddCategoryBtn').init(
            text='Category', icon=Icons.PLUS, slot=self.add_category
        ))
        vlayout.addWidget(Label(self, 'LeftMenuCategoriesLabel').init(
            text='Categories'
        ))
        if not len(categories):
            vlayout.addWidget(Label(self, 'NoCategoriesLbl').init(
                text='You don\'t have any categories yet', alignment=Qt.AlignVCenter | Qt.AlignHCenter,
                wrap=True, size=Sizes.NoCategoriesLbl
            ), alignment=VLayout.CenterCenter)
        else:
            sarea = ScrollArea(self, 'CategoriesScrollArea', False, True).init(
                layout_t=VLayout, alignment=VLayout.Top, spacing=5
            )
            for category in categories:
                sarea.widget().layout().addWidget(CountableButton(self).init(
                    icon=Icons.STAR, text=category['title'], total=len(category['items']),
                    slot=lambda checked, c=category: self.show_category(c)
                ))
            vlayout.addWidget(sarea)
        self.setLayout(vlayout)
        return self

    def show_category(self, category: dict[str, Any]):
        central_pages = self.parent().parent().findChild(QStackedWidget, 'CentralPages')
        central_pages.setCurrentIndex(0)
        items = central_pages.currentWidget()
        layout = items.findChild(QScrollArea, 'ItemsScrollArea').widget().layout()
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

    def app(self):
        return self.parent().parent().parent()
