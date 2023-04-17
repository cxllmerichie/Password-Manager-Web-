from PyQt5.QtWidgets import QScrollArea, QWidget, QLayout
from PyQt5.QtCore import Qt

from .frame import Frame
from .layout import Layout
from ._wrapper import Wrapper


class ScrollArea(QScrollArea, Wrapper):
    def __init__(self, parent: QWidget, name: str, visible: bool = True):
        QScrollArea.__init__(self, parent)
        Wrapper.__init__(self, parent, name, visible)

    def init(
            self, *,
            horizontal: bool = True, vertical: bool = True, orientation: Qt.Orientation,
            margins: tuple[int, ...] = (0, 0, 0, 0), spacing: int = 0, alignment: Qt.Alignment = None
    ) -> 'ScrollArea':
        if not horizontal:
            self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        if not vertical:
            self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setWidgetResizable(True)
        widget = Frame(self, f'{self.objectName()}Widget')

        layout = Layout.oriented(orientation, widget, f'{self.objectName()}WidgetLayout').init(
            margins=margins, spacing=spacing, alignment=alignment
        )
        self.setWidget(widget.init(layout=layout))
        return self

    def clear(self):
        self.widget().layout().clear()
