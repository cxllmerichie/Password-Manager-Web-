from aioqui.widgets import Label, Layout, ScrollArea, Button, Frame, Parent
from aioqui.widgets.custom import TotalButton, SearchBar
from aioqui.widgets.extensions import SplitterWidgetExt
from aioqui.asynq import asyncSlot
from aioqui.types import Icon
from aioqui.types.enums import SizePolicy
from aioqui import CONTEXT
from contextlib import suppress

from ..misc import ICONS, SIZES, API
from ..components import LabelExtended
from .. import qss


class LeftMenu(SplitterWidgetExt, Frame):
    def __init__(self, parent: Parent):
        Frame.__init__(self, parent, self.__class__.__name__, qss=(
            qss.menu_left.css,
            qss.components.scroll,
            qss.components.search
        ))
        SplitterWidgetExt.__init__(self, 300, SIZES.LeftMenuMin, SIZES.LeftMenuMax)

    async def init(self) -> 'LeftMenu':
        self.setLayout(await Layout.vertical().init(
            spacing=5, margins=(0, 10, 0, 10), alignment=Layout.Top,
            items=[
                await LabelExtended(self, 'ItemsLbl').init(
                    text='Items', margins=(0, 0, 0, SIZES.LeftMenuTitlesMargin[3])
                ), Layout.Center,
                await TotalButton(self, 'AllItemsBtn').init(
                    icon=ICONS.HOME, text='All items', on_click=CONTEXT.CentralItems.show_all
                ),
                await TotalButton(self, 'FavItemsBtn').init(
                    icon=Icon(ICONS.STAR.icon, ICONS.HOME.size), text='Favourite',
                    on_click=CONTEXT.CentralItems.show_favourite
                ),
                await LabelExtended(self, 'CategoriesLbl').init(
                    text='Categories', margins=SIZES.LeftMenuTitlesMargin
                ), Layout.Center,
                SearchBar(self, visible=False),
                await Label(self, 'NoCategoriesLbl', False).init(
                    text='You don\'t have any categories yet', wrap=True,
                    policy=(Label.Expanding, Label.Expanding), alignment=Layout.HCenter
                ), Layout.HCenter,
                await ScrollArea(self, 'ScrollArea', False).init(
                    hspolicy=ScrollArea.AlwaysOff, orientation=ScrollArea.Vertical, alignment=Layout.Top, spacing=5,
                    hpolicy=SizePolicy.Minimum
                ),
                await Button(self, 'AddCategoryBtn').init(
                    text='Category', icon=ICONS.PLUS, on_click=CONTEXT.RightPagesCategory.show_create
                )
            ]
        ))
        return self

    @asyncSlot()
    async def searchbar_textchanged(self):
        layout = self.ScrollArea.widget().layout()
        text = self.SearchBar.text()
        for i in range(layout.count()):
            widget = layout.itemAt(i).widget()
            visible = True
            if widget.__class__.__name__ == 'LabelExtended':
                visible = widget.label.text()[0].lower() == text[0].lower() if len(text) else True
            elif widget.__class__.__name__ in 'TotalButton':
                visible = text.lower() in widget.TextLbl.text().lower()
            widget.setVisible(visible)
        with suppress(AttributeError):  # self.FavouriteLbl may not exist if none of items['is_favourite']
            self.FavouriteLbl.setVisible(not text)

    @asyncSlot()
    async def refresh_categories(self):
        categories = await API.get_categories()
        self.SearchBar.setVisible(not_empty := bool(len(categories)))
        self.ScrollArea.setVisible(not_empty)
        self.NoCategoriesLbl.setVisible(not not_empty)
        self.AllItemsBtn.AllItemsBtnTotalLbl.setText(str(sum([len(c['items']) for c in categories])))
        self.FavItemsBtn.FavItemsBtnTotalLbl.setText(
            str(sum([len([1 for i in c['items'] if i['is_favourite']]) for c in categories])))
        self.ScrollArea.clear()
        if not not_empty:
            return
        categories = sorted(categories, key=lambda c: (not c['is_favourite'], c['title'], c['description']))
        if any([category['is_favourite'] for category in categories]):
            self.ScrollArea.addWidget(await LabelExtended(self, 'FavouriteLbl').init(
                text='Favourite', margins=SIZES.LeftMenuLettersMargin
            ))
        letters = []
        for category in categories:
            if not category['is_favourite'] and (letter := category['title'][0]) not in letters:
                letters.append(letter)
                self.ScrollArea.addWidget(await LabelExtended(self, 'LetterLbl').init(
                    text=letter, margins=SIZES.LeftMenuLettersMargin
                ))
            self.ScrollArea.addWidget(await TotalButton(self).init(
                icon=Icon(category['icon'], SIZES.MenuBtnIcon), text=category['title'], total=len(category['items']),
                on_click=lambda checked=False, _category=category: CONTEXT.RightPagesCategory.show_category(_category)
            ))
        await self.SearchBar.init(
            on_change=self.searchbar_textchanged, placeholder='Search',
            completer=SearchBar.Completer(
                self.SearchBar, qss=qss.components.search, items=[c['title'] for c in categories]
            )
        )
