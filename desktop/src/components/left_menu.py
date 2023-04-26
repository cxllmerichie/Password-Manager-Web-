from qcontextapi.widgets import Label, Layout, ScrollArea, Button, Widget, Spacer
from qcontextapi.extensions import SplitterWidgetExt
from qcontextapi.utils import Icon
from qcontextapi.customs import MenuButton, SearchBar, LabelExtended
from qcontextapi import CONTEXT
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt
from typing import Any
from contextlib import suppress

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
                LabelExtended(self, 'LeftMenuItemsLabel').init(
                    text='Items', margins=(0, 0, 0, SIZES.LeftMenuTitlesMargin[3])
                ), Layout.Center,
                AllItemsBtn := MenuButton(self).init(
                    icon=ICONS.HOME, text='All items', slot=CONTEXT.CP_Items.show_all
                ),
                FavItemsBtn := MenuButton(self).init(
                    icon=Icon(ICONS.STAR.icon, ICONS.HOME.size), text='Favourite', slot=CONTEXT.CP_Items.show_favourite
                ),
                LabelExtended(self, 'LeftMenuCategoriesLabel').init(
                    text='Categories', margins=SIZES.LeftMenuTitlesMargin
                ), Layout.Center,
                Label(self, 'NoCategoriesLbl', False).init(
                    text='You don\'t have any categories yet', alignment=Qt.AlignVCenter | Qt.AlignHCenter, wrap=True
                ),
                SearchBar(self),
                ScrollArea(self, 'CategoriesScrollArea', False).init(
                    horizontal=False, vertical=True, orientation=Layout.Vertical, alignment=Layout.Top, spacing=5,
                    policy=(Layout.Minimum, Layout.Expanding)
                ),
                # Spacer(False, True),
                Button(self, 'AddCategoryBtn').init(
                    text='Category', icon=ICONS.PLUS, slot=CONTEXT.RP_Category.show_create
                )
            ]
        ))
        self.AllItemsBtn = AllItemsBtn
        self.FavItemsBtn = FavItemsBtn
        self.refresh_categories()
        return self

    def searchbar_textchanged(self):
        layout = self.CategoriesScrollArea.widget().layout()
        text = self.SearchBar.text()
        for i in range(layout.count()):
            widget = layout.itemAt(i).widget()
            visible = True
            if widget.__class__.__name__ == 'LabelExtended':
                visible = widget.label.text()[0].lower() == text[0].lower() if len(text) else True
            elif widget.__class__.__name__ in 'MenuButton':
                visible = text.lower() in widget.text_lbl.text().lower()
            widget.setVisible(visible)
        with suppress(AttributeError):  # self.FavouriteLbl may not exist if none of items['is_favourite']
            self.FavouriteLbl.setVisible(not text)

    def refresh_categories(self):
        layout = self.CategoriesScrollArea.widget().layout()
        layout.clear()
        categories = API.categories
        if not len(categories):
            self.CategoriesScrollArea.setVisible(False)
            return self.NoCategoriesLbl.setVisible(True)
        letters = []
        categories = sorted(categories, key=lambda c: (not c['is_favourite'], c['title'], c['description']))
        if any([category['is_favourite'] for category in categories]):
            layout.addWidget(LabelExtended(self, 'FavouriteLbl').init(
                text='Favourite', margins=SIZES.LeftMenuLettersMargin
            ))
        for category in categories:
            if not category['is_favourite'] and (letter := category['title'][0]) not in letters:
                letters.append(letter)
                layout.addWidget(LabelExtended(self, 'LetterLbl').init(
                    text=letter, margins=SIZES.LeftMenuLettersMargin
                ))
            layout.addWidget(MenuButton(self).init(
                icon=Icon(category['icon'], SIZES.MenuBtnIcon), text=category['title'], total=len(category['items']),
                slot=lambda checked, _category=category: CONTEXT.RP_Category.show_category(_category)
            ))
        self.SearchBar.init(
            textchanged=self.searchbar_textchanged, placeholder='Search', stylesheet=css.components.search,
            items=[category['title'] for category in categories] + letters
        )
        self.NoCategoriesLbl.setVisible(False)
        self.CategoriesScrollArea.setVisible(True)
        self.AllItemsBtn.MenuButtonTotalLbl.setText(str(sum([len(c['items']) for c in categories])))
        self.FavItemsBtn.MenuButtonTotalLbl.setText(str(sum([len([1 for i in c['items'] if i['is_favourite']]) for c in categories])))
