from PyQt5.QtWidgets import QWidget, QSpacerItem, QSizePolicy
from PyQt5.QtGui import QMouseEvent
from PyQt5.QtCore import Qt

from ..widgets import Button, Label, Layout, Frame
from ..misc import Icons, Sizes
from .. import css


class Panel(QWidget):
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self.setObjectName(self.__class__.__name__)
        self.setStyleSheet(css.panel.css)
        self.setAttribute(Qt.WA_StyledBackground, True)

    def init(self) -> 'Panel':
        self.setLayout(Layout.horizontal().init(
            spacing=10,
            items=[
                Button(self, 'ToggleLeftMenuBtn').init(
                    slot=lambda: self.parent().findChild(QWidget, 'LeftMenu').toggle(), icon=Icons.MENU
                ), Qt.AlignLeft,
                Label(self, 'PanelTitleLbl').init(
                    text='Password Manager'
                ), Qt.AlignLeft,
                Label(self, 'PanelTitleLbl').init(
                    icon=Icons.APP
                ), Qt.AlignLeft,
                QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum),
                Frame(self, 'PanelFrame').init(
                    layout=Layout.horizontal().init(
                        alignment=Layout.Right,
                        items=[
                            Button(self, 'PanelMinimizeBtn').init(
                                icon=Icons.MINIMIZE, size=Sizes.PanelNavigationBtn, slot=self.app().showMinimized
                            ),
                            Button(self, 'PanelRestoreBtn').init(
                                icon=Icons.RESTORE, size=Sizes.PanelNavigationBtn,
                                slot=lambda: self.app().showNormal() if self.app().isMaximized() else self.app().showMaximized()
                            ),
                            Button(self, 'PanelCloseBtn').init(
                                icon=Icons.CROSS, size=Sizes.PanelNavigationBtn, slot=self.app().close
                            )
                        ]
                    )
                )
            ]
        ))
        return self

    def app(self) -> 'App':
        return self.parent().parent().parent()

    def mousePressEvent(self, event: QMouseEvent) -> None:
        self.app().setProperty('position', event.globalPos())

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        delta = event.globalPos() - self.app().property('position')
        self.app().move(self.app().x() + delta.x(), self.app().y() + delta.y())
        self.app().setProperty('position', event.globalPos())
