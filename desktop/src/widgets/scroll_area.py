from PyQt5.QtWidgets import QScrollArea, QWidget
from PyQt5.QtCore import Qt, QObject
from typing import Sequence

from .frame import Frame
from .layout import Layout
from ._wrapper import Wrapper


class ScrollArea(Wrapper, QScrollArea):
    def __init__(self, parent: QWidget, name: str, visible: bool = True):
        QScrollArea.__init__(self, parent)
        Wrapper.__init__(self, parent, name, visible)

    def init(
            self, *,
            horizontal: bool = True, vertical: bool = True, orientation: Qt.Orientation,
            margins: tuple[int, ...] = (0, 0, 0, 0), spacing: int = 0, alignment: Qt.Alignment = None,
            items: Sequence[QObject] = ()
    ) -> 'ScrollArea':
        if not horizontal:
            self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        if not vertical:
            self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setWidgetResizable(True)
        self.setWidget(Frame(self, f'{self.objectName()}Widget').init(
            layout=Layout.oriented(orientation, None, f'{self.objectName()}WidgetLayout').init(
                margins=margins, spacing=spacing, alignment=alignment, items=items
            )
        ))
        return self

    def clear(self):
        self.widget().layout().clear()
