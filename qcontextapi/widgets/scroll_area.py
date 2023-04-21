from PyQt5.QtWidgets import QScrollArea, QWidget
from PyQt5.QtCore import Qt, QObject
from typing import Sequence

from .frame import Frame
from .layout import Layout
from ..extensions import ContextObjectExt


class ScrollArea(ContextObjectExt, QScrollArea):
    def __init__(self, parent: QWidget, name: str, visible: bool = True):
        QScrollArea.__init__(self, parent)
        ContextObjectExt.__init__(self, parent, name, visible)

    def init(
            self, *,
            orientation: Qt.Orientation, horizontal: bool = True, vertical: bool = True,
            margins: tuple[int, ...] = (0, 0, 0, 0), spacing: int = 0, alignment: Qt.Alignment = None,
            items: Sequence[QObject] = ()
    ) -> 'ScrollArea':
        if not horizontal:
            self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        if not vertical:
            self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setWidgetResizable(True)
        frame = Frame(self, f'{self.objectName()}Widget')
        self.setWidget(frame.init(
            layout=Layout.oriented(orientation, frame, f'{frame.objectName()}Layout').init(
                margins=margins, spacing=spacing, alignment=alignment, items=items
            )
        ))
        return self

    def clear(self):
        self.widget().layout().clear()
