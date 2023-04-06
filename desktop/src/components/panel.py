from PyQt5.QtWidgets import QWidget, QSpacerItem, QSizePolicy
from PyQt5.QtGui import QMouseEvent
from PyQt5.QtCore import Qt

from ..css import panel
from ..widgets import Button, Label, HLayout, Frame
from ..misc import Icons, Sizes


class Panel(QWidget):
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self.setObjectName(self.__class__.__name__)
        self.setStyleSheet(panel.css)
        self.setAttribute(Qt.WA_StyledBackground, True)

    async def init(self) -> 'Panel':
        self.setLayout(await self.__layout())
        return self

    async def __layout(self) -> HLayout:
        layout = await HLayout().init(spacing=10)
        layout.addWidget(await Button(self, 'ToggleLeftMenuBtn').init(
            slot=lambda: self.parent().findChild(QWidget, 'LeftMenu').toggle(), icon=Icons.MENU
        ), alignment=Qt.AlignLeft)
        layout.addWidget(await Label(self, 'PanelTitleLbl').init(
            text='Password Manager'
        ), alignment=Qt.AlignLeft)
        layout.addWidget(await Label(self, 'PanelTitleLbl').init(
            icon=Icons.APP
        ), alignment=Qt.AlignLeft)
        layout.addItem(QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum))

        hlayout = await HLayout().init(alignment=HLayout.Right)
        hlayout.addWidget(await Button(self, 'PanelMinimizeBtn').init(
            icon=Icons.MINIMIZE, size=Sizes.PanelNavigationBtn, slot=self.app.showMinimized
        ))
        hlayout.addWidget(await Button(self, 'PanelRestoreBtn').init(
            icon=Icons.RESTORE, size=Sizes.PanelNavigationBtn,
            slot=lambda: self.app.showNormal() if self.app.isMaximized() else self.app.showMaximized()
        ))
        hlayout.addWidget(await Button(self, 'PanelCloseBtn').init(
            icon=Icons.CROSS, size=Sizes.PanelNavigationBtn, slot=self.app.close
        ))
        layout.addWidget(await Frame(self).init(layout=hlayout))
        return layout

    @property
    def app(self) -> 'App':
        return self.parent().parent().parent()  # App.AppPages.AppView.Panel

    def mousePressEvent(self, event: QMouseEvent) -> None:
        self.app.setProperty('position', event.globalPos())

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        delta = event.globalPos() - self.app.property('position')
        self.app.move(self.app.x() + delta.x(), self.app.y() + delta.y())
        self.app.setProperty('position', event.globalPos())
