from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt, pyqtSlot
from typing import Any

from ..widgets import Label, Layout, ScrollArea, Button, SideMenu, Widget, ui
from ..misc import Icons, api
from .. import css
from ..custom import MenuButton
from .central_pages import CP_Item


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
                AllItemsBtn := MenuButton(self).init(
                    icon=Icons.HOME, text='All items', total=0
                ), Qt.AlignLeft,
                FavItemsBtn := MenuButton(self).init(
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
        self.refresh_categories(categories)
        return self

    def refresh_categories(self, categories: list[dict[str, Any]]):
        if not len(categories):
            self.CategoriesScrollArea.setVisible(False)
            return self.NoCategoriesLbl.setVisible(True)
        layout = self.CategoriesScrollArea.widget().layout()
        layout.clear()
        for category in categories:
            layout.addWidget(
                MenuButton(self).init(
                    icon=Icons.from_bytes(category['icon']).adjusted(size=Icons.HOME.size), text=category['title'],
                    total=len(category['items']), slot=lambda checked, _category=category: self.show_category(_category)
                )
            )
        self.NoCategoriesLbl.setVisible(False)
        self.CategoriesScrollArea.setVisible(True)
        self.AllItemsBtn.MenuButtonTotalLbl.setText(str(sum([len(c['items']) for c in categories])))
        self.FavItemsBtn.MenuButtonTotalLbl.setText(str(sum([len([1 for i in c['items'] if i['is_favourite']]) for c in categories])))

    def show_category(self, category: dict[str, Any]):
        ui.MainView.RightPages.setCurrentWidget(ui.RP_Category)
        ui.MainView.RightPages.expand()
        ui.RP_Category.show_category(category)

        ui.CentralPages.setCurrentWidget(ui.CP_Items)
        layout = ui.CP_Items.ItemsScrollArea.widget().layout()
        layout.clear()
        for item in category['items']:
            layout.addWidget(CP_Item(ui.CP_Items, item, ui.RP_Item.show_item).init())

    def show_item(self, item: dict[str, Any]):
        ui.MainView.RightPages.setCurrentWidget(ui.RP_Item)
        ui.MainView.RightPages.expand()
        ui.RP_Item.show_item(item)

    @pyqtSlot()
    def add_category(self):
        ui.MainView.RightPages.setCurrentWidget(ui.RP_Category)
        ui.RP_Category.show_create_category()
        ui.MainView.RightPages.expand()
