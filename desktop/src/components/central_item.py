from qcontextapi.widgets import Layout, Label, Frame, Button
from PyQt5.QtWidgets import QWidget
from qcontextapi.misc import Icon
from qcontextapi import CONTEXT
from typing import Any

from .. import stylesheets


class CentralItem(Frame):
    def __init__(self, parent: QWidget):
        super().__init__(parent, self.__class__.__name__, stylesheet=stylesheets.central_item.css)

    async def init(self, item: dict[str, Any]) -> 'CentralItem':
        self.item = item
        await super().init(layout=await Layout.horizontal(self, 'ItemLayout').init(
            margins=(10, 10, 10, 10), alignment=Layout.Left, spacing=20,
            items=[
                await Label(self, 'ItemIconLbl').init(
                    icon=Icon(item['icon'], (50, 50))
                ), Layout.Left,
                await Layout.vertical().init(
                    items=[
                        await Label(self, 'ItemTitleLbl').init(
                            text=item['title'], policy=(Layout.Expanding, Layout.Minimum), elided=True
                        ),
                        await Label(self, 'ItemDescriptionLbl').init(
                            text=item['description'], policy=(Layout.Expanding, Layout.Minimum), elided=True
                        )
                    ]
                )
            ]
        ), policy=(Layout.Expanding, Layout.Minimum))
        # workaround to make `self` clickable
        emitter = await Button(self, 'CentralItemEmitterBtn', False).init(
            slot=lambda: CONTEXT.RightPagesItem.show_item(item)
        )
        self.mousePressEvent = lambda event: emitter.click()
        return self
