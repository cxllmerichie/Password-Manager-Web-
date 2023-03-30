from PyQt5.QtWidgets import QVBoxLayout, QFrame, QWidget, QPushButton
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon
from typing import Any

from ..css import left_menu
from ..widgets import Button, Label, HLayout
from ..assets import Icons, Sizes, Icon


class CountableButton(QPushButton):
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self.setObjectName(self.__class__.__name__)

    async def init(self, icon: Icon, text, count: int | list[Any, ...],
                   *, name: str = None, alignment: Qt.Alignment = None) -> 'CountableButton':
        layout = HLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setAlignment(Qt.AlignLeft)
        layout.addWidget(await Button(self, 'CountableButtonIcon').init(
            size=icon.size, icon=icon
        ), alignment=Qt.AlignLeft)
        layout.addWidget(await Label(self, 'CountableButtonLbl').init(
            text=text, alignment=alignment
        ), alignment=Qt.AlignLeft)
        layout.addWidget(await Label(self, 'CountableButtonCountLbl').init(
            text=str(count) if isinstance(count, int) else str(len(count))
        ), alignment=Qt.AlignRight)
        self.setLayout(layout)
        if name:
            self.setObjectName(name)
        return self


class LeftMenu(QWidget):
    def __init__(self, parent: QWidget, width: int):
        super().__init__(parent)
        self._width = width
        self.setObjectName(self.__class__.__name__)
        self.setStyleSheet(left_menu.css)
        self.setAttribute(Qt.WA_StyledBackground, True)

    async def __layout(self) -> QVBoxLayout:
        vbox = QVBoxLayout()
        vbox.setAlignment(Qt.AlignTop)
        vbox.setSpacing(10)
        vbox.addWidget(await CountableButton(self).init(
            Icons.HOME, 'All items', 0, alignment=Qt.AlignBottom | Qt.AlignLeft
        ), alignment=Qt.AlignLeft)
        vbox.addWidget(await CountableButton(self).init(
            Icons.FAVOURITE, 'Favourites', 0, alignment=Qt.AlignBottom | Qt.AlignLeft
        ), alignment=Qt.AlignLeft)
        # vbox.addWidget(await Label(self).init(
        #     'Categories', 'LeftMenuCategoriesLabel'
        # ))
        return vbox

    async def init(self) -> 'LeftMenu':
        self.setLayout(await self.__layout())
        self.expand()
        return self

    def expand(self) -> None:
        self.setFixedWidth(self._width)

    def shrink(self) -> None:
        self.setFixedWidth(0)

    def toggle(self) -> None:
        self.expand() if self.width() == 0 else self.shrink()
