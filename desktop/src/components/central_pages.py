from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt
from typing import Any

from ..widgets import ScrollArea, Layout, Label, Frame, StackedWidget, ui
from ..misc import Icons, api
from .. import css


class CP_Item(Frame):
    def __init__(self, parent: QWidget):
        super().__init__(parent, self.__class__.__name__,
                         stylesheet=css.central_pages.cp_item)

    def init(self, item: dict[str, Any], slot: callable) -> 'CP_Item':
        self.setLayout(Layout.horizontal(self, 'ItemLayout').init(
            margins=(10, 10, 10, 10), alignment=Layout.Left, spacing=20,
            items=[
                Label(self, 'ItemIconLbl').init(
                    icon=Icons.from_bytes(item['icon']).adjusted(size=(50, 50))
                ), Layout.Left,
                Layout.vertical().init(
                    items=[
                        Label(self, 'ItemTitleLbl').init(
                            text=item['title'], policy=(Layout.Expanding, Layout.Minimum), elided=True
                        ),
                        Label(self, 'ItemDescriptionLbl').init(
                            text=item['description'], elided=True
                        )
                    ]
                )
            ]
        ))
        self.mousePressEvent = lambda event: slot(item)
        return self


class CP_Items(ScrollArea):
    def __init__(self, parent: QWidget):
        super().__init__(parent, self.__class__.__name__)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.setStyleSheet(css.central_pages.cp_items + css.components.scroll)
        self.categories = []

    def refresh_items(self, items: list[dict[str, Any]]):
        letters = set()
        layout = self.widget().layout()
        self.clear()
        items = sorted(items, key=lambda i: (not i['is_favourite'], i['title'], i['description']))
        if any([item['is_favourite'] for item in items]):
            layout.addWidget(Label(self, 'FavouriteLbl').init(
                text='Favourite'
            ))
        for item in items:
            if not item['is_favourite'] and (letter := item['title'][0]) not in letters:
                letters.add(letter)
                layout.addWidget(Label(self, 'LetterLbl').init(
                    text=letter
                ))
            layout.addWidget(CP_Item(self).init(item, ui.RP_Item.show_item))

    def show_all(self):
        items = []
        for category in self.categories:
            items += category['items']
        self.refresh_items(items)

    def show_favourite(self):
        items = []
        for category in self.categories:
            items += list(filter(lambda x: x['is_favourite'], category['items']))
        self.refresh_items(items)


class CentralPages(StackedWidget):
    def __init__(self, parent):
        super().__init__(parent, self.__class__.__name__,
                         stylesheet=css.central_pages.css)

    def init(self) -> 'CentralPages':
        self.addWidget(cp_items := CP_Items(self).init(
            orientation=Layout.Vertical, alignment=Layout.TopCenter, spacing=10, margins=(30, 10, 30, 10),
            horizontal=False
        ))

        self.setCurrentWidget(cp_items)
        return self
