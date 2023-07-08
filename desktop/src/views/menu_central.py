from aioqui.widgets import ScrollArea, Layout, Label, Frame, Parent
from aioqui.widgets.extensions import SplitterWidgetExt
from aioqui.widgets.custom import SearchBar
from aioqui.asynq import asyncSlot
from contextlib import suppress
from typing import Any

from ..misc import api, COLORS
from .. import qss
from ..components.cp_item import CentralItem


class CentralItems(SplitterWidgetExt, Frame):
    def __init__(self, parent: Parent):
        Frame.__init__(self, parent, self.__class__.__name__, qss=(
            qss.menu_central.css,
            qss.components.scroll.replace('REPLACE', '30'),
            qss.components.search.replace('REPLACE', COLORS.LIGHT)
        ))
        SplitterWidgetExt.__init__(self, collapsible=False)

    async def init(self):
        await super().init(layout=await Layout.vertical().init(
            spacing=20, margins=(30, 10, 30, 0),
            items=[
                SearchBar(self, visible=False), Layout.TopCenter,
                await ScrollArea(self, 'ScrollArea', False).init(
                    hspolicy=ScrollArea.AlwaysOff, orientation=ScrollArea.Vertical,
                    alignment=Layout.TopCenter, spacing=10
                ),
                await Label(self, 'NoCategoriesLbl', False).init(
                    wrap=True, alignment=Layout.Center,
                    text='This category does not have items yet'
                ), Layout.Center,
                await Label(self, 'HintLbl1').init(
                    wrap=True, alignment=Layout.Center,
                    text='Select some category in the left menu to see it\'s items',
                ), Layout.Center,
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
            if widget.__class__.__name__ == 'Label':
                visible = widget.text()[0].lower() == text[0].lower() if len(text) else True
            elif widget.__class__.__name__ in 'CentralItem':
                visible = text.lower() in widget.TitleLbl.text().lower()
            widget.setVisible(visible)
        with suppress(AttributeError):
            self.FavouriteLbl.setVisible(not text)

    @asyncSlot()
    async def refresh_items(self, items: list[dict[str, Any]]):
        self.HintLbl1.setVisible(False)
        self.SearchBar.setVisible(not_empty := bool(len(items)))
        self.ScrollArea.setVisible(not_empty)
        self.NoCategoriesLbl.setVisible(not not_empty)
        if not not_empty:
            return
        letters = []
        self.ScrollArea.clear()
        if any([item['is_favourite'] for item in items]):
            self.ScrollArea.addWidget(await Label(self, 'FavouriteLbl').init(text='Favourite'))
        for item in items:
            if not item['is_favourite'] and (letter := item['title'][0]) not in letters:
                letters.append(letter)
                self.ScrollArea.addWidget(await Label(self, 'LetterLbl').init(text=letter))
            self.ScrollArea.addWidget(await CentralItem(self).init(item))
        await self.SearchBar.init(
            on_change=self.searchbar_textchanged, placeholder='Search', fix_width=500,
            completer=SearchBar.Completer(
                self.SearchBar, items=[i['title'] for i in items], qss=qss.components.search
            )
        )

    @asyncSlot()
    async def show_all(self):
        items = []
        for category in await api.get_categories():
            items += await api.get_items(category['id'])
        await self.refresh_items(sorted(items, key=lambda i: (not i['is_favourite'], i['title'], i['description'])))

    @asyncSlot()
    async def show_favourite(self):
        items = []
        for category in await api.get_categories():
            items += list(filter(lambda x: x['is_favourite'], await api.get_items(category['id'])))
        await self.refresh_items(sorted(items, key=lambda i: (not i['is_favourite'], i['title'], i['description'])))
