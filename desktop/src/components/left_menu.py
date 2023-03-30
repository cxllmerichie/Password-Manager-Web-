from PyQt5.QtWidgets import QVBoxLayout, QFrame, QWidget, QPushButton
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon
from typing import Any

from ..css import left_menu
from ..widgets import Button, Label, HLayout
from ..assets import Icon, Size


class CountableButton(QPushButton):
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self.setObjectName(self.__class__.__name__)

    async def init(self, icon: str, isize: QSize, text, count: int | list[Any, ...],
                   *, name: str = None, alignment: Qt.Alignment = None) -> 'CountableButton':
        layout = HLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setAlignment(Qt.AlignLeft)
        layout.addWidget(await Button(self).init(
            '', 'CountableButtonIcon', size=isize, icon=QIcon(icon), isize=isize
        ), alignment=Qt.AlignLeft)
        layout.addWidget(await Label(self).init(
            text, 'CountableButtonLbl', alignment
        ), alignment=Qt.AlignLeft)
        layout.addWidget(await Label(self).init(
            str(count) if isinstance(count, int) else str(len(count)), 'CountableButtonCountLbl'
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
            Icon.HOME, Size.HomeIcon, 'All items', 0, alignment=Qt.AlignBottom | Qt.AlignLeft
        ), alignment=Qt.AlignLeft)
        vbox.addWidget(await CountableButton(self).init(
            Icon.FAVOURITE, Size.StarIcon, 'Favourites', 0, alignment=Qt.AlignBottom | Qt.AlignLeft
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
