from aioqui.widgets import Button, Label, Layout, Frame, Panel as PanelBase, Spacer, Parent
from PySide6.QtCore import Qt
from aioqui import CONTEXT
from PySide6.QtGui import QMouseEvent
from contextlib import suppress

from ..misc import ICONS, SIZES
from .. import qss


class Panel(PanelBase):
    def __init__(self, parent: Parent):
        PanelBase.__init__(self, parent, self.__class__.__name__, qss=qss.panel.css)

    async def init(self) -> 'Panel':
        self.setLayout(await Layout.horizontal().init(
            spacing=10,
            items=[
                await Button(self, 'ToggleMenuBtn').init(
                    icon=ICONS.MENU,
                    on_click=lambda: CONTEXT.LeftMenu.toggle()  # lambda used since `LeftMenu` does not exist yet
                ), Layout.Left,
                await Label(self, 'TitleLbl').init(
                    text='Password Manager'
                ), Layout.Left,
                await Label(self, 'TitleImg').init(
                    icon=ICONS.APP
                ), Layout.Left,
                Spacer(Spacer.Expanding, Spacer.Expanding),
                await Frame(self, 'PanelFrame').init(
                    layout=await Layout.horizontal().init(
                        alignment=Layout.Right,
                        items=[
                            await Button(self, 'MinimizeBtn').init(
                                icon=ICONS.MINIMIZE, fix_size=SIZES.PanelNavigationBtn,
                                on_click=self.core.showMinimized
                            ),
                            await Button(self, 'RestoreBtn').init(
                                icon=ICONS.RESTORE, fix_size=SIZES.PanelNavigationBtn,
                                on_click=lambda: self.core.showNormal() if self.core.isMaximized() else self.core.showMaximized()
                            ),
                            await Button(self, 'CloseBtn').init(
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
        if event.buttons() is Qt.LeftButton:
            with suppress(Exception):  # when moving core through panel clicking on panel child ui item
                delta = event.globalPos() - self.core.property('position')
                self.core.move(self.core.x() + delta.x(), self.core.y() + delta.y())
                self.core.setProperty('position', event.globalPos())
