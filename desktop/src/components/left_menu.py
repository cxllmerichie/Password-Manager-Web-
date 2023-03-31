from PyQt5.QtWidgets import QWidget, QPushButton
from PyQt5.QtCore import Qt
from typing import Any

from ..css import left_menu
from ..widgets import Button, Label, HLayout, VLayout, SideMenu
from ..const import Icons, Sizes, Icon


class CountableButton(QPushButton):
    def __init__(self, parent: QWidget, name: str = None):
        super().__init__(parent)
        self.setObjectName(self.__class__.__name__)
        if name:
            self.setObjectName(name)

    async def init(
            self, *,
            icon: Icon, text, total: int | list[Any, ...],
            alignment: Qt.Alignment = None, slot: callable = lambda: None
    ) -> 'CountableButton':
        layout = await HLayout().init(margins=(10, 0, 0, 0), spacing=10, alignment=Qt.AlignLeft)
        layout.addWidget(await Button(self, 'CountableButtonIcon').init(
            size=icon.size, icon=icon, disabled=True
        ))
        layout.addWidget(await Label(self, 'CountableButtonLbl').init(
            text=text, alignment=alignment
        ))
        layout.addWidget(await Label(self, 'CountableButtonCountLbl').init(
            text=str(total) if isinstance(total, int) else str(len(total))
        ), alignment=Qt.AlignRight)
        self.setLayout(layout)
        self.clicked.connect(slot)
        return self


class LeftMenu(QWidget, SideMenu):
    def __init__(self, parent: QWidget, width: int):
        super(QWidget, self).__init__(parent)
        self.setObjectName(self.__class__.__name__)
        self.setStyleSheet(left_menu.css)
        self.setAttribute(Qt.WA_StyledBackground, True)

        self.expand_to = width

    async def __layout(self) -> VLayout:
        vlayout = await VLayout().init(spacing=5, margins=(10, 10, 0, 0), alignment=Qt.AlignTop)
        vlayout.addWidget(await Label(self, 'LeftMenuItemsLabel').init(
            text='Items'
        ), alignment=Qt.AlignVCenter)
        vlayout.addWidget(await CountableButton(self).init(
            icon=Icons.HOME, text='All items', total=0
        ), alignment=Qt.AlignLeft)
        vlayout.addWidget(await CountableButton(self).init(
            icon=Icons.FAVOURITE, text='Favourites', total=0
        ), alignment=Qt.AlignLeft)
        vlayout.addWidget(await Label(self, 'LeftMenuCategoriesLabel').init(
            text='Categories'
        ))
        categories = ['Facebook', 'Instagram', 'Telegram', 'Github', 'JetBrains', 'Binance', 'WhiteBit', 'CryptoCom',
                      'Gmail', 'Google', 'Outlook', 'PyPi', 'Kuna.io']
        for category in categories:
            vlayout.addWidget(await CountableButton(self).init(
                icon=Icons.FAVOURITE, text=category, total=0
            ), alignment=Qt.AlignLeft)
        if not len(categories):
            vlayout.addWidget(await Label(self, 'NoCategoriesLbl').init(
                text='You don\'t have any categories yet', alignment=Qt.AlignVCenter | Qt.AlignHCenter,
                wrap=True, size=Sizes.NoCategoriesLbl
            ), alignment=VLayout.CenterCenter)
        return vlayout

    async def init(self) -> 'LeftMenu':
        self.setLayout(await self.__layout())
        self.shrink()
        return self
