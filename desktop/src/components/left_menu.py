from PyQt5.QtWidgets import QStackedWidget, QWidget, QVBoxLayout
from PyQt5.QtCore import Qt, QSize

from ..css import left_menu
from ..widgets import Button, Label
from ..assets import Icon


class LeftMenu(QWidget):
    def __init__(self, parent: QWidget, width: int):
        super().__init__(parent)
        self._width = width
        self.setObjectName(self.__class__.__name__)
        self.setStyleSheet(left_menu.css)
        self.setAttribute(Qt.WA_StyledBackground, True)

    async def __layout(self) -> QVBoxLayout:
        vbox = QVBoxLayout()
        vbox.setContentsMargins(10, 30, 10, 10)
        vbox.setAlignment(Qt.AlignLeft)
        vbox.setSpacing(10)
        vbox.addWidget(await Button(self).init(
            'All items', 'LeftMenuAllItemsBtn', icon=Icon.home, isize=QSize(20, 20)
        ), alignment=Qt.AlignLeft)
        vbox.addWidget(await Button(self).init(
            'Favourites', 'LeftMenuFavouritesBtn', icon=Icon.star, isize=QSize(20, 20)
        ))
        vbox.addWidget(await Label(self).init(
            'Categories', 'LeftMenuCategoriesLabel'
        ))
        return vbox

    async def init(self) -> 'LeftMenu':
        self.setLayout(await self.__layout())
        await self.expand()
        return self

    async def expand(self):
        self.setFixedWidth(self._width)

    async def shrink(self):
        self.setFixedWidth(0)
