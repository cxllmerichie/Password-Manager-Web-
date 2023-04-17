from PyQt5.QtGui import QMouseEvent
from PyQt5.QtWidgets import QWidget, QFrame
from typing import Any

from ..widgets import ScrollArea, Layout, Label
from ..misc import Icons
from .. import css


class CentralItem(QFrame):
    def __init__(self, parent: QWidget, item: dict[str, Any], slot: callable):
        super().__init__(parent)
        self.setObjectName('CentralItem')
        self.item = item
        self.slot = slot

    def mousePressEvent(self, event: QMouseEvent) -> None:
        self.slot(self.item)

    def init(self) -> 'CentralItem':
        layout = Layout.horizontal().init()
        layout.addWidget(Label(self, 'IconLbl').init(
            icon=Icons.from_bytes(self.item['icon']).adjusted(size=(40, 40))
        ))
        vbox = Layout.vertical().init()
        vbox.addWidget(Label(self, 'TitleLbl').init(
            text=self.item['title']
        ))
        vbox.addWidget(Label(self, 'DescriptionLbl').init(
            text=self.item['description']
        ))
        layout.addLayout(vbox)
        self.setLayout(layout)
        return self


class Items(QWidget):
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self.setStyleSheet(css.items.css)

    def init(self) -> 'Items':
        layout = Layout.vertical().init()
        layout.addWidget(ScrollArea(self, 'ItemsScrollArea', False).init(
            orientation=Layout.Vertical, alignment=Layout.TopCenter, spacing=10
        ))
        self.setLayout(layout)
        return self
