from qcontext.widgets import Button, Label, Layout, Frame, Widget, Spacer
from qcontext import CONTEXT
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QMouseEvent
from contextlib import suppress

from ..misc import ICONS, SIZES
from .. import stylesheets


class Panel(Widget):
    def __init__(self, parent: QWidget):
        super().__init__(parent, self.__class__.__name__, stylesheet=stylesheets.panel.css)

    async def init(self) -> 'Panel':
        self.setLayout(await Layout.horizontal().init(
            spacing=10,
            items=[
                await Button(self, 'ToggleLeftMenuBtn').init(
                    slot=lambda: CONTEXT.LeftMenu.toggle(), icon=ICONS.MENU
                ), Layout.Left,
                await Label(self, 'PanelTitleLbl').init(
                    text='Password Manager'
                ), Layout.Left,
                await Label(self, 'PanelTitleLbl').init(
                    icon=ICONS.APP
                ), Layout.Left,
                Spacer(True, True),
                await Frame(self, 'PanelFrame').init(
                    layout=await Layout.horizontal().init(
                        alignment=Layout.Right,
                        items=[
                            await Button(self, 'PanelMinimizeBtn').init(
                                icon=ICONS.MINIMIZE, size=SIZES.PanelNavigationBtn, slot=self.core.showMinimized
                            ),
                            await Button(self, 'PanelRestoreBtn').init(
                                icon=ICONS.RESTORE, size=SIZES.PanelNavigationBtn,
                                slot=lambda: self.core.showNormal() if self.core.isMaximized() else self.core.showMaximized()
                            ),
                            await Button(self, 'PanelCloseBtn').init(
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
