from aioqui.widgets import Button, Label, Layout, Frame, Widget, Spacer, Parent
from aioqui import CONTEXT
from PySide6.QtGui import QMouseEvent
from contextlib import suppress

from ..misc import ICONS, SIZES
from .. import stylesheets


class Panel(Widget):
    def __init__(self, parent: Parent):
        super().__init__(parent, self.__class__.__name__, stylesheet=stylesheets.panel.css)

    async def init(self) -> 'Panel':
        self.setLayout(await Layout.horizontal().init(
            spacing=10,
            items=[
                await Button(self, 'ToggleLeftMenuBtn').init(
                    icon=ICONS.MENU, events=Button.Events(on_click=CONTEXT.LeftMenu.toggle)
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
                                icon=ICONS.MINIMIZE, sizes=Button.Sizes(fixed_size=SIZES.PanelNavigationBtn),
                                events=Button.Events(on_click=self.core.showMinimized)
                            ),
                            await Button(self, 'PanelRestoreBtn').init(
                                icon=ICONS.RESTORE, sizes=Button.Sizes(fixed_size=SIZES.PanelNavigationBtn),
                                events=Button.Events(on_click=lambda: self.core.showNormal() if self.core.isMaximized() else self.core.showMaximized())
                            ),
                            await Button(self, 'PanelCloseBtn').init(
                                icon=ICONS.CROSS, sizes=Button.Sizes(fixed_size=SIZES.PanelNavigationBtn),
                                events=Button.Events(on_click=self.core.close)
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
        with suppress(Exception):  # when moving core through panel clicking on panel child ui item
            delta = event.globalPos() - self.core.property('position')
            self.core.move(self.core.x() + delta.x(), self.core.y() + delta.y())
            self.core.setProperty('position', event.globalPos())
