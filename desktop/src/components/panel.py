from PySide6.QtCore import Qt
from aioqui.widgets import Button, Label, Layout, Frame, Panel as CPanel, Spacer, Parent
from aioqui import CONTEXT
from PySide6.QtGui import QMouseEvent
from contextlib import suppress

from ..misc import ICONS, SIZES
from .. import qss


class Panel(CPanel):
    def __init__(self, parent: Parent):
        CPanel.__init__(self, parent, self.__class__.__name__, qss=qss.panel.css)

    async def init(self) -> 'Panel':
        self.setLayout(await Layout.horizontal().init(
            spacing=10,
            items=[
                await Button(self, 'ToggleLeftMenuBtn').init(
                    icon=ICONS.MENU,
                    on_click=lambda: CONTEXT.LeftMenu.toggle()  # lambda used since `LeftMenu` does not exist yet
                ), Layout.Left,
                await Label(self, 'PanelTitleLbl').init(
                    text='Password Manager'
                ), Layout.Left,
                await Label(self, 'PanelTitleLbl').init(
                    icon=ICONS.APP
                ), Layout.Left,
                Spacer(Spacer.Expanding, Spacer.Expanding),
                await Frame(self, 'PanelFrame').init(
                    layout=await Layout.horizontal().init(
                        alignment=Layout.Right,
                        items=[
                            await Button(self, 'PanelMinimizeBtn').init(
                                icon=ICONS.MINIMIZE, fix_size=SIZES.PanelNavigationBtn,
                                on_click=self.core.showMinimized
                            ),
                            await Button(self, 'PanelRestoreBtn').init(
                                icon=ICONS.RESTORE, fix_size=SIZES.PanelNavigationBtn,
                                on_click=lambda: self.core.showNormal() if self.core.isMaximized() else self.core.showMaximized()
                            ),
                            await Button(self, 'PanelCloseBtn').init(
                                icon=ICONS.CROSS, fix_size=SIZES.PanelNavigationBtn, on_click=self.core.close
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
        if event.buttons() & Qt.LeftButton:
            with suppress(Exception):  # when moving core through panel clicking on panel child ui item
                delta = event.globalPos() - self.core.property('position')
                self.core.move(self.core.x() + delta.x(), self.core.y() + delta.y())
                self.core.setProperty('position', event.globalPos())
