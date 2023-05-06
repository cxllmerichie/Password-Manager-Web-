from qcontextapi.widgets import ScrollArea, Layout, Label, Frame
from qcontextapi.customs import SearchBar
from PyQt5.QtWidgets import QWidget
from typing import Any

from ..misc import API
from .. import css
from ..components.central_item import CentralItem


class CentralItems(Frame):
    def __init__(self, parent: QWidget):
        Frame.__init__(self, parent, self.__class__.__name__,
                       stylesheet=css.central_items.css + css.components.scroll + css.components.search)

    def init(self):
        super().init(layout=Layout.vertical().init(
            spacing=20, margins=(30, 10, 30, 10),
            items=[
                SearchBar(self, visible=False),
                ScrollArea(self, 'ItemsScrollArea', False).init(
                    orientation=Layout.Vertical, alignment=Layout.TopCenter, spacing=10, horizontal=False
                ),
                Label(self, 'NoCategoriesLbl', False).init(
                    text='This category does not have items yet', wrap=True, alignment=Layout.Center
                ), Layout.Center,
                Label(self, 'HintLbl1').init(
                    text='Select some category in the left menu to see it\'s items', wrap=True, alignment=Layout.Center
                ), Layout.Center,
            ]
        ))
        return self

    def searchbar_textchanged(self):
        layout = self.ItemsScrollArea.widget().layout()
        text = self.SearchBar.text()
        for i in range(layout.count()):
            widget = layout.itemAt(i).widget()
            visible = True
            if widget.__class__.__name__ == 'Label':
                visible = widget.text()[0].lower() == text[0].lower() if len(text) else True
            elif widget.__class__.__name__ in 'CP_Item':
                visible = text.lower() in widget.ItemTitleLbl.text().lower()
            widget.setVisible(visible)
        # with suppress(AttributeError):
        #     self.FavouriteLbl.setVisible(not text)

    def refresh_items(self, items: list[dict[str, Any]] = None):
        if items is None:
            items = API.items
        self.HintLbl1.setVisible(False)
        if not len(items):
            self.SearchBar.setVisible(False)
            self.ItemsScrollArea.setVisible(False)
            return self.NoCategoriesLbl.setVisible(True)
        letters = []
        layout = self.ItemsScrollArea.widget().layout()
        self.ItemsScrollArea.clear()
        items = sorted(items, key=lambda i: (not i['is_favourite'], i['title'], i['description']))
        if any([item['is_favourite'] for item in items]):
            layout.addWidget(Label(self, 'FavouriteLbl').init(
                text='Favourite'
            ))
        for item in items:
            if not item['is_favourite'] and (letter := item['title'][0]) not in letters:
                letters.append(letter)
                layout.addWidget(Label(self, 'LetterLbl').init(
                    text=letter
                ))
            layout.addWidget(CentralItem(self).init(item))
        self.SearchBar.init(
            textchanged=self.searchbar_textchanged, placeholder='Search', stylesheet=css.components.search,
            items=[item['title'] for item in items] + letters
        )
        self.SearchBar.setVisible(True)
        self.NoCategoriesLbl.setVisible(False)
        self.ItemsScrollArea.setVisible(True)

    def show_all(self):
        items = []
        for category in API.categories:
            items += category['items']
        self.refresh_items(items)

    def show_favourite(self):
        items = []
        for category in API.categories:
            items += list(filter(lambda x: x['is_favourite'], category['items']))
        self.refresh_items(items)