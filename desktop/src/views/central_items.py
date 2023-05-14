from aioqui.widgets import ScrollArea, Layout, Label, Frame, Parent
from aioqui.widgets.custom import SearchBar
from aioqui.qasyncio import asyncSlot
from typing import Any
from contextlib import suppress

from ..misc import API
from .. import stylesheets
from ..components.central_item import CentralItem


class CentralItems(Frame):
    def __init__(self, parent: Parent):
        Frame.__init__(self, parent, self.__class__.__name__, stylesheet=stylesheets.central_items.css +
                                                                         stylesheets.components.scroll +
                                                                         stylesheets.components.search)

    async def init(self):
        await super().init(layout=await Layout.vertical().init(
            spacing=20, margins=(30, 10, 30, 10),
            items=[
                SearchBar(self, visible=False),
                await ScrollArea(self, 'ItemsScrollArea', False).init(
                    hpolicy=ScrollArea.AlwaysOff, orientation=ScrollArea.Vertical,
                    alignment=Layout.TopCenter, spacing=10
                ),
                await Label(self, 'NoCategoriesLbl', False).init(
                    wrap=True, sizes=Label.Sizes(alignment=Layout.Center),
                    text='This category does not have items yet'
                ), Layout.Center,
                await Label(self, 'HintLbl1').init(
                    wrap=True, sizes=Label.Sizes(alignment=Layout.Center),
                    text='Select some category in the left menu to see it\'s items',
                ), Layout.Center,
            ]
        ))
        return self

    @asyncSlot()
    async def searchbar_textchanged(self):
        layout = self.ItemsScrollArea.widget().layout()
        text = self.SearchBar.text()
        for i in range(layout.count()):
            widget = layout.itemAt(i).widget()
            visible = True
            if widget.__class__.__name__ == 'Label':
                visible = widget.text()[0].lower() == text[0].lower() if len(text) else True
            elif widget.__class__.__name__ in 'CentralItem':
                visible = text.lower() in widget.ItemTitleLbl.text().lower()
            widget.setVisible(visible)
        with suppress(AttributeError):
            self.FavouriteLbl.setVisible(not text)

    @asyncSlot()
    async def refresh_items(self, items: list[dict[str, Any]] = None):
        if items is None:
            items = API.items
        self.HintLbl1.setVisible(False)
        self.SearchBar.setVisible(not_empty := bool(len(items)))
        self.ItemsScrollArea.setVisible(not_empty)
        self.NoCategoriesLbl.setVisible(not not_empty)
        if not not_empty:
            return
        letters = []
        self.ItemsScrollArea.clear()
        items = sorted(items, key=lambda i: (not i['is_favourite'], i['title'], i['description']))
        if any([item['is_favourite'] for item in items]):
            self.ItemsScrollArea.addWidget(await Label(self, 'FavouriteLbl').init(text='Favourite'))
        for item in items:
            if not item['is_favourite'] and (letter := item['title'][0]) not in letters:
                letters.append(letter)
                self.ItemsScrollArea.addWidget(await Label(self, 'LetterLbl').init(text=letter))
            self.ItemsScrollArea.addWidget(await CentralItem(self).init(item))
        await self.SearchBar.init(
            events=SearchBar.Events(on_change=self.searchbar_textchanged), placeholder='Search',
            completer=SearchBar.Completer(
                self.SearchBar, items=[i['title'] for i in items] + letters, stylesheet=stylesheets.components.search
            )
        )

    @asyncSlot()
    async def show_all(self):
        items = []
        for category in API.categories:
            items += category['items']
        await self.refresh_items(items)

    @asyncSlot()
    async def show_favourite(self):
        items = []
        for category in API.categories:
            items += list(filter(lambda x: x['is_favourite'], category['items']))
        await self.refresh_items(items)
