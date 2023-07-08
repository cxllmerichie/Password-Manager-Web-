from aioqui.widgets import Label, Layout, ScrollArea, Button, Frame, Parent
from aioqui.widgets.custom import TotalButton, SearchBar
from aioqui.widgets.extensions import SplitterWidgetExt
from aioqui.types import Icon, SizePolicy
from aioqui.asynq import asyncSlot
from contextlib import suppress
from aioqui import CONTEXT

from ..misc import ICONS, SIZES, api
from ..components import LabelExtended
from .. import qss


class LeftMenu(SplitterWidgetExt, Frame):
    def __init__(self, parent: Parent):
        Frame.__init__(self, parent, self.__class__.__name__, qss=(
            qss.menu_left.css,
            qss.components.scroll,
            qss.components.search
        ))
        SplitterWidgetExt.__init__(self, SIZES.LeftMenuFix, SIZES.LeftMenuMin, SIZES.LeftMenuMax)

    async def init(self) -> 'LeftMenu':
        self.setLayout(await Layout.vertical().init(
            spacing=5, margins=(0, 10, 0, 10), alignment=Layout.Top,
            items=[
                await LabelExtended(self, 'ItemsLbl').init(
                    text='Items', margins=(0, 0, 0, SIZES.LeftMenuTitlesMargin[3])
                ), Layout.Center,
                await TotalButton(self, 'AllItemsBtn').init(
                    icon=ICONS.HOME, text='All items', on_click=lambda: CONTEXT.CentralItems.show_all()
                ),
                await TotalButton(self, 'FavItemsBtn').init(
                    icon=Icon(ICONS.STAR_FILL.icon, ICONS.HOME.size), text='Favourite',
                    on_click=lambda: CONTEXT.CentralItems.show_favourite()
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
                    text='Category', icon=ICONS.PLUS, on_click=lambda: CONTEXT.RightPagesCategory.show_create()
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
        categories = await api.get_categories()
        self.SearchBar.setVisible(not_empty := bool(len(categories)))
        self.ScrollArea.setVisible(not_empty)
        self.NoCategoriesLbl.setVisible(not not_empty)
        total, favourite = 0, 0
        for items in (all_items := {c['id']: await api.get_items(c['id']) for c in categories}).values():
            total += len(items)
            for item in items:
                favourite += int(item['is_favourite'])
        self.AllItemsBtn.AllItemsBtnTotalLbl.setText(str(total))
        self.FavItemsBtn.FavItemsBtnTotalLbl.setText(str(favourite))
        self.ScrollArea.clear()
        if not not_empty:
            return
        if any([category['is_favourite'] for category in categories]):
            self.ScrollArea.addWidget(await LabelExtended(self, 'FavouriteLbl').init(
                text='Favourite', margins=SIZES.LeftMenuLettersMargin
            ))
        letters = []
        for c in categories:
            if not c['is_favourite'] and (letter := c['title'][0]) not in letters:
                letters.append(letter)
                self.ScrollArea.addWidget(await LabelExtended(self, 'LetterLbl').init(
                    text=letter, margins=SIZES.LeftMenuLettersMargin
                ))
            self.ScrollArea.addWidget(await TotalButton(self).init(
                icon=Icon(c['icon'], SIZES.MenuBtnIcon), text=c['title'], total=len(all_items[c['id']]),
                on_click=lambda checked=False, _category=c: CONTEXT.RightPagesCategory.show_category(_category)
            ))
        await self.SearchBar.init(
            on_change=self.searchbar_textchanged, placeholder='Search',
            completer=SearchBar.Completer(
                self.SearchBar, qss=qss.components.search, items=[c['title'] for c in categories]
            )
        )
