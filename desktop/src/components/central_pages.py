from PyQt5.QtWidgets import QWidget
from typing import Any

from ..widgets import ScrollArea, Layout, Label, Frame, Widget, StackedWidget, ui
from ..misc import Icons
from .. import css


class CP_Item(Frame):
    def __init__(self, parent: QWidget):
        super().__init__(parent, self.__class__.__name__,
                         stylesheet=css.central_pages.cp_item)

    def init(self, item: dict[str, Any], slot: callable) -> 'CP_Item':
        self.setLayout(Layout.horizontal(self, 'ItemLayout').init(
            items=[
                Label(self, 'ItemIconLbl').init(
                    icon=Icons.from_bytes(item['icon']).adjusted(size=(50, 50))
                ),
                Layout.vertical().init(
                    items=[
                        Label(self, 'ItemTitleLbl').init(
                            text=item['title']
                        ),
                        Label(self, 'ItemDescriptionLbl').init(
                            text=item['description']
                        )
                    ]
                )
            ]
        ))
        self.mousePressEvent = lambda event: slot(item)
        return self


class CP_Items(ScrollArea):
    def __init__(self, parent: QWidget):
        super().__init__(parent, self.__class__.__name__)
        self.setStyleSheet(css.central_pages.cp_items + css.components.scroll)

    def refresh_items(self, items: list[dict[str, Any]]):
        layout = self.widget().layout()
        self.clear()
        for item in items:
            layout.addWidget(CP_Item(self).init(item, ui.RP_Item.show_item))


class CentralPages(StackedWidget):
    def __init__(self, parent):
        super().__init__(parent, self.__class__.__name__,
                         stylesheet=css.central_pages.css)

    def init(self) -> 'CentralPages':
        self.addWidget(cp_items := CP_Items(self).init(
            orientation=Layout.Vertical, alignment=Layout.TopCenter, spacing=10
        ))

        self.setCurrentWidget(cp_items)
        return self
