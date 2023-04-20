from qcontextapi.widgets import Label, Layout, ScrollArea, Button, Widget
from qcontextapi.extensions import SideMenuExt
from qcontextapi.utils import Icon
from qcontextapi import ui
from qcontextapi.customs import MenuButton
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt
from typing import Any

from ..misc import Icons, api, Sizes
from .. import css


class LeftMenu(SideMenuExt, Widget):
    def __init__(self, parent: QWidget, width: int):
        Widget.__init__(self, parent, self.__class__.__name__,
                        stylesheet=css.left_menu.css + css.components.scroll)
        SideMenuExt.__init__(self, width, Qt.Horizontal)

    def init(self) -> 'LeftMenu':
        categories = api.get_categories()
        self.setLayout(Layout.vertical().init(
            spacing=5, margins=(0, 10, 0, 10), alignment=Qt.AlignTop,
            items=[
                Label(self, 'LeftMenuItemsLabel').init(
                    text='Items'
                ), Qt.AlignVCenter,
                AllItemsBtn := MenuButton(self).init(
                    icon=Icons.HOME, text='All items', total=0, slot=ui.CP_Items.show_all
                ),
                FavItemsBtn := MenuButton(self).init(
                    icon=Icons.STAR.adjusted(size=Icons.HOME.size), text='Favourite', slot=ui.CP_Items.show_favourite,
                    total=sum([len([1 for item in category['items'] if item['is_favourite']]) for category in categories])
                ),
                Button(self, 'AddCategoryBtn').init(
                    text='Category', icon=Icons.PLUS, slot=ui.RP_Category.show_create
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
                    icon=Icon.from_bytes(category['icon']).adjusted(size=Sizes.MenuBtnIcon.size), text=category['title'],
                    total=len(category['items']), slot=lambda checked, c=category: ui.RP_Category.show_category(c)
                )
            )
        self.NoCategoriesLbl.setVisible(False)
        self.CategoriesScrollArea.setVisible(True)
        self.AllItemsBtn.MenuButtonTotalLbl.setText(str(sum([len(c['items']) for c in categories])))
        self.FavItemsBtn.MenuButtonTotalLbl.setText(str(sum([len([1 for i in c['items'] if i['is_favourite']]) for c in categories])))
        # cache categories for `CentralPages`
        self.MainView.CentralPages.CP_Items.categories = categories
