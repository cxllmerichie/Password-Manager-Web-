from PyQt5.QtWidgets import QWidget, QSpacerItem, QSizePolicy
from PyQt5.QtGui import QMouseEvent
from PyQt5.QtCore import Qt

from ..widgets import Button, Label, Layout, Frame, Widget
from ..misc import Icons, Sizes
from .. import css


class Panel(Widget):
    def __init__(self, parent: QWidget):
        super().__init__(parent, self.__class__.__name__, stylesheet=css.panel.css)

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
                                icon=Icons.MINIMIZE, size=Sizes.PanelNavigationBtn, slot=self.core.showMinimized
                            ),
                            Button(self, 'PanelRestoreBtn').init(
                                icon=Icons.RESTORE, size=Sizes.PanelNavigationBtn,
                                slot=lambda: self.core.showNormal() if self.core.isMaximized() else self.core.showMaximized()
                            ),
                            Button(self, 'PanelCloseBtn').init(
                                icon=Icons.CROSS, size=Sizes.PanelNavigationBtn, slot=self.core.close
                            )
                        ]
                    )
                )
            ]
        ))
        return self

    def mousePressEvent(self, event: QMouseEvent) -> None:
        self.core.setProperty('position', event.globalPos())

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        delta = event.globalPos() - self.core.property('position')
        self.core.move(self.core.x() + delta.x(), self.core.y() + delta.y())
        self.core.setProperty('position', event.globalPos())
