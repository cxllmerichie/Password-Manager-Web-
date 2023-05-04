from qcontextapi.widgets import Button, Label, Layout, Frame, Widget, Spacer
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QMouseEvent
from PyQt5.QtCore import Qt
from contextlib import suppress

from ..misc import ICONS, SIZES
from .. import css


class Panel(Widget):
    def __init__(self, parent: QWidget):
        super().__init__(parent, self.__class__.__name__, stylesheet=css.panel.css)

    def init(self) -> 'Panel':
        self.setLayout(Layout.horizontal().init(
            spacing=10,
            items=[
                Button(self, 'ToggleLeftMenuBtn').init(
                    slot=lambda: self.parent().findChild(QWidget, 'LeftMenu').toggle(), icon=ICONS.MENU
                ), Qt.AlignLeft,
                Label(self, 'PanelTitleLbl').init(
                    text='Password Manager'
                ), Qt.AlignLeft,
                Label(self, 'PanelTitleLbl').init(
                    icon=ICONS.APP
                ), Qt.AlignLeft,
                Spacer(True, True),
                Frame(self, 'PanelFrame').init(
                    layout=Layout.horizontal().init(
                        alignment=Layout.Right,
                        items=[
                            Button(self, 'PanelMinimizeBtn').init(
                                icon=ICONS.MINIMIZE, size=SIZES.PanelNavigationBtn, slot=self.core.showMinimized
                            ),
                            Button(self, 'PanelRestoreBtn').init(
                                icon=ICONS.RESTORE, size=SIZES.PanelNavigationBtn,
                                slot=lambda: self.core.showNormal() if self.core.isMaximized() else self.core.showMaximized()
                            ),
                            Button(self, 'PanelCloseBtn').init(
                                icon=ICONS.CROSS, size=SIZES.PanelNavigationBtn, slot=self.core.close
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
        with suppress(Exception):
            delta = event.globalPos() - self.core.property('position')
            self.core.move(self.core.x() + delta.x(), self.core.y() + delta.y())
            self.core.setProperty('position', event.globalPos())
