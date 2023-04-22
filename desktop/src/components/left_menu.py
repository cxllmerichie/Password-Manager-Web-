from qcontextapi.widgets import Label, Layout, ScrollArea, Button, Widget
from qcontextapi.extensions import SplitterWidgetExt
from qcontextapi.utils import Icon
from qcontextapi.customs import MenuButton, SearchBar
from qcontextapi import CONTEXT
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt
from typing import Any

from ..misc import ICONS, SIZES, API
from .. import css


class LeftMenu(SplitterWidgetExt, Widget):
    def __init__(self, parent: QWidget):
        Widget.__init__(self, parent, self.__class__.__name__,
                        stylesheet=css.left_menu.css + css.components.scroll + css.components.search)
        SplitterWidgetExt.__init__(self, 300, SIZES.LeftMenuMin, SIZES.LeftMenuMax, Qt.Horizontal)

    def init(self, categories: list[dict[str, Any]] = API.get_categories()) -> 'LeftMenu':
        self.setLayout(Layout.vertical().init(
            spacing=5, margins=(0, 10, 0, 10), alignment=Qt.AlignTop,
            items=[
                SearchBar(self).init(
                    update=self.update, placeholder='Search',
                    items=[]
                ),
                Label(self, 'LeftMenuItemsLabel').init(
                    text='Items'
                ), Qt.AlignVCenter,
                AllItemsBtn := MenuButton(self).init(
                    icon=ICONS.HOME, text='All items', total=0, slot=CONTEXT.CP_Items.show_all
                ),
                FavItemsBtn := MenuButton(self).init(
                    icon=Icon(ICONS.STAR.icon, ICONS.HOME.size), text='Favourite', slot=CONTEXT.CP_Items.show_favourite,
                    total=0
                ),
                Button(self, 'AddCategoryBtn').init(
                    text='Category', icon=ICONS.PLUS, slot=CONTEXT.RP_Category.show_create
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
        self.refresh_categories()
        return self

    def refresh_categories(self):
        layout = self.CategoriesScrollArea.widget().layout()
        layout.clear()
        categories = API.categories
        if not len(categories):
            self.CategoriesScrollArea.setVisible(False)
            return self.NoCategoriesLbl.setVisible(True)
        letters = set()
        categories = sorted(categories, key=lambda c: (not c['is_favourite'], c['title'], c['description']))
        if any([category['is_favourite'] for category in categories]):
            layout.addWidget(Label(self, 'FavouriteLbl').init(
                text='Favourite'
            ))
        for category in categories:
            if not category['is_favourite'] and (letter := category['title'][0]) not in letters:
                letters.add(letter)
                layout.addWidget(Label(self, 'LetterLbl').init(
                    text=letter
                ))
            layout.addWidget(MenuButton(self).init(
                icon=Icon(category['icon'], SIZES.MenuBtnIcon), text=category['title'], total=len(category['items']),
                slot=lambda checked, _category=category: CONTEXT.RP_Category.show_category(_category)
            ))
        self.NoCategoriesLbl.setVisible(False)
        self.CategoriesScrollArea.setVisible(True)
        self.AllItemsBtn.MenuButtonTotalLbl.setText(str(sum([len(c['items']) for c in categories])))
        self.FavItemsBtn.MenuButtonTotalLbl.setText(str(sum([len([1 for i in c['items'] if i['is_favourite']]) for c in categories])))
