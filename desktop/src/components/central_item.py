from qcontextapi.widgets import Layout, Label, Frame
from PyQt5.QtWidgets import QWidget
from qcontextapi.misc import Icon
from qcontextapi import CONTEXT
from typing import Any

from .. import stylesheets


class CentralItem(Frame):
    def __init__(self, parent: QWidget):
        super().__init__(parent, self.__class__.__name__, stylesheet=stylesheets.central_item.css)

    def init(self, item: dict[str, Any]) -> 'CentralItem':
        super().init(layout=Layout.horizontal(self, 'ItemLayout').init(
            margins=(10, 10, 10, 10), alignment=Layout.Left, spacing=20,
            items=[
                Label(self, 'ItemIconLbl').init(
                    icon=Icon(item['icon'], (50, 50))
                ), Layout.Left,
                Layout.vertical().init(
                    items=[
                        Label(self, 'ItemTitleLbl').init(
                            text=item['title'], policy=(Layout.Expanding, Layout.Minimum), elided=True
                        ),
                        Label(self, 'ItemDescriptionLbl').init(
                            text=item['description'], policy=(Layout.Expanding, Layout.Minimum), elided=True
                        )
                    ]
                )
            ]
        ), policy=(Layout.Expanding, Layout.Minimum))
        self.mousePressEvent = lambda event: CONTEXT.RightPagesItem.show_item(item)
        return self
