from qcontextapi.widgets import Label, Layout, ScrollArea, Button, Widget
from qcontextapi.customs import MenuButton, SearchBar, LabelExtended
from qcontextapi.extensions import SplitterWidgetExt
from qcontextapi.misc import Icon, utils
from qcontextapi import CONTEXT
from PyQt5.QtCore import Qt
from qasync import asyncSlot
from PyQt5.QtWidgets import QWidget
from contextlib import suppress
from typing import Any

from ..misc import ICONS, SIZES, API
from .. import stylesheets


class LeftMenu(SplitterWidgetExt, Widget):
    def __init__(self, parent: QWidget):
        Widget.__init__(self, parent, self.__class__.__name__, stylesheet=stylesheets.left_menu.css +
                                                                          stylesheets.components.scroll +
                                                                          stylesheets.components.search)
        SplitterWidgetExt.__init__(self, 300, SIZES.LeftMenuMin, SIZES.LeftMenuMax, Qt.Horizontal)

    async def init(self) -> 'LeftMenu':
        self.setLayout(await Layout.vertical().init(
            spacing=5, margins=(0, 10, 0, 10), alignment=Qt.AlignTop,
            items=[
                await LabelExtended(self, 'LeftMenuItemsLabel').init(
                    text='Items', margins=(0, 0, 0, SIZES.LeftMenuTitlesMargin[3])
                ), Layout.Center,
                await MenuButton(self, 'AllItemsBtn').init(
                    icon=ICONS.HOME, text='All items', slot=CONTEXT.CentralItems.show_all
                ),
                await MenuButton(self, 'FavItemsBtn').init(
                    icon=Icon(ICONS.STAR.icon, ICONS.HOME.size), text='Favourite',
                    slot=CONTEXT.CentralItems.show_favourite
                ),
                await LabelExtended(self, 'LeftMenuCategoriesLabel').init(
                    text='Categories', margins=SIZES.LeftMenuTitlesMargin
                ), Layout.Center,
                SearchBar(self, visible=False),
                await Label(self, 'NoCategoriesLbl', False).init(
                    text='You don\'t have any categories yet', alignment=Qt.AlignHCenter, wrap=True,
                    policy=(Layout.Expanding, Layout.Expanding)
                ), Layout.HCenter,
                await ScrollArea(self, 'CategoriesScrollArea', False).init(
                    horizontal=False, vertical=True, orientation=Layout.Vertical, alignment=Layout.Top, spacing=5,
                    policy=(Layout.Minimum, Layout.Expanding)
                ),
                await Button(self, 'AddCategoryBtn').init(
                    text='Category', icon=ICONS.PLUS, slot=CONTEXT.RightPagesCategory.show_create
                )
            ]
        ))
        return self

    @asyncSlot()
    async def searchbar_textchanged(self):
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

    @asyncSlot()
    async def refresh_categories(self, categories: list[dict[str, Any]] = None):
        layout = self.CategoriesScrollArea.widget().layout()
        layout.clear()
        if categories:
            API.categories = categories
        if not (categories := API.categories):
            categories = await API.get_categories()
        self.SearchBar.setVisible(bool(len(categories)))
        if not len(categories):
            self.CategoriesScrollArea.setVisible(False)
            return self.NoCategoriesLbl.setVisible(True)
        letters = []
        categories = sorted(categories, key=lambda c: (not c['is_favourite'], c['title'], c['description']))
        if any([category['is_favourite'] for category in categories]):
            layout.addWidget(await LabelExtended(self, 'FavouriteLbl').init(
                text='Favourite', margins=SIZES.LeftMenuLettersMargin
            ))
        for category in categories:
            if not category['is_favourite'] and (letter := category['title'][0]) not in letters:
                letters.append(letter)
                layout.addWidget(await LabelExtended(self, 'LetterLbl').init(
                    text=letter, margins=SIZES.LeftMenuLettersMargin
                ))
            layout.addWidget(await MenuButton(self).init(
                icon=Icon(category['icon'], SIZES.MenuBtnIcon), text=category['title'], total=len(category['items']),
                slot=lambda checked, _category=category: CONTEXT.RightPagesCategory.show_category(_category)
            ))
        await self.SearchBar.init(
            textchanged=self.searchbar_textchanged, placeholder='Search', stylesheet=stylesheets.components.search,
            items=[category['title'] for category in categories] + letters
        )
        self.NoCategoriesLbl.setVisible(False)
        self.CategoriesScrollArea.setVisible(True)
        self.AllItemsBtn.AllItemsBtnTotalLbl.setText(str(sum([len(c['items']) for c in categories])))
        self.FavItemsBtn.FavItemsBtnTotalLbl.setText(str(sum([len([1 for i in c['items'] if i['is_favourite']]) for c in categories])))
