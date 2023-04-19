from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QMouseEvent
from typing import Any

from ..widgets import ScrollArea, Layout, Label, Frame, Widget, StackedWidget
from ..misc import Icons
from .. import css


class CentralPagesItem(Frame):
    def __init__(self, parent: QWidget, item: dict[str, Any], slot: callable):
        super().__init__(parent, self.__class__.__name__, stylesheet=css.cp_items.central_pages_items)

        self.item = item
        self.slot = slot

    def mousePressEvent(self, event: QMouseEvent) -> None:
        self.slot(self.item)

    def init(self) -> 'CentralPagesItem':
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


class CentralPagesItems(Widget):
    def __init__(self, parent: QWidget):
        super().__init__(parent, self.__class__.__name__, stylesheet=css.cp_items.css)

    def init(self) -> 'CentralPagesItems':
        self.setLayout(Layout.vertical().init(
            items=[
                ScrollArea(self, 'ItemsScrollArea', False).init(
                    orientation=Layout.Vertical, alignment=Layout.TopCenter, spacing=10
                )
            ]
        ))
        return self


class CentralPages(StackedWidget):
    def __init__(self, parent):
        super().__init__(parent, self.__class__.__name__)
        self.setStyleSheet(css.menu_central_pages.css)

    def init(self) -> 'CentralPages':
        self.addWidget(CentralPagesItems(self).init())
        self.setCurrentIndex(0)
        return self
