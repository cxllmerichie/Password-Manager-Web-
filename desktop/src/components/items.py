import typing

from PyQt5.QtGui import QMouseEvent
from PyQt5.QtWidgets import QWidget, QFrame, QPushButton

from ..widgets import ScrollArea, Frame, VLayout, HLayout, Label
from ..css import items
from ..misc import Icons


class CentralItem(QFrame):
    def __init__(self, parent: QWidget, item: dict[str, typing.Any], slot: callable):
        super().__init__(parent)
        self.setObjectName('CentralItem')
        self.item = item
        self.slot = slot

    def mousePressEvent(self, event: QMouseEvent) -> None:
        self.slot(self.item)

    def init(self) -> 'CentralItem':
        layout = HLayout().init()
        layout.addWidget(Label(self, 'IconLbl').init(
            icon=Icons.from_bytes(self.item['icon']).adjusted(size=(40, 40))
        ))
        vbox = VLayout().init()
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
        self.setStyleSheet(items.css)

    def init(self) -> 'Items':
        layout = VLayout().init()
        layout.addWidget(ScrollArea(self, 'ItemsScrollArea', False).init(
            layout_t=VLayout, alignment=VLayout.HCenterTop, spacing=10
        ))
        self.setLayout(layout)
        return self
