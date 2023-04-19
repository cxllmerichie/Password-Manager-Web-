from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QMouseEvent
from typing import Any

from ..widgets import ScrollArea, Layout, Label, Frame, Widget, StackedWidget, ui
from ..misc import Icons
from .. import css


class CP_Item(Frame):
    def __init__(self, parent: QWidget, item: dict[str, Any], slot: callable):
        super().__init__(parent, self.__class__.__name__,
                         stylesheet=css.cp_items.central_pages_items)

        self.item = item
        self.slot = slot

    def mousePressEvent(self, event: QMouseEvent) -> None:
        self.slot(self.item)

    def init(self) -> 'CP_Item':
        self.setLayout(Layout.horizontal().init(
            items=[
                Label(self, 'IconLbl').init(
                    icon=Icons.from_bytes(self.item['icon']).adjusted(size=(40, 40))
                ),
                Layout.vertical().init(
                    items=[
                        Label(self, 'TitleLbl').init(
                            text=self.item['title']
                        ),
                        Label(self, 'DescriptionLbl').init(
                            text=self.item['description']
                        )
                    ]
                )
            ]
        ))
        return self


class CP_Items(Widget):
    def __init__(self, parent: QWidget):
        super().__init__(parent, self.__class__.__name__, stylesheet=css.cp_items.css)

    def init(self) -> 'CP_Items':
        self.setLayout(Layout.vertical().init(
            items=[
                ScrollArea(self, 'ItemsScrollArea', False).init(
                    orientation=Layout.Vertical, alignment=Layout.TopCenter, spacing=10
                )
            ]
        ))
        return self

    def refresh_items(self, items: list[dict[str, Any]]):
        layout = self.ItemsScrollArea.widget().layout()
        layout.clear()
        for item in items:
            layout.addWidget(CP_Item(self, item, ui.RP_Item.show_item).init())


class CentralPages(StackedWidget):
    def __init__(self, parent):
        super().__init__(parent, self.__class__.__name__, stylesheet=css.central_pages.css)

    def init(self) -> 'CentralPages':
        self.addWidget(cp_items := CP_Items(self).init())

        self.setCurrentWidget(cp_items)
        return self
