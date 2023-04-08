from PyQt5.QtWidgets import QScrollArea, QWidget
from PyQt5.QtCore import Qt

from ..widgets import Frame, VLayout, HLayout


class ScrollArea(QScrollArea):
    def __init__(self, parent: QWidget, name: str, horizontal: bool = True, vertical: bool = True):
        super().__init__(parent)
        self.setObjectName(name)
        if not horizontal:
            self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        if not vertical:
            self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

    def init(
            self, *,
            vertical: bool = True, items: list[QWidget]
    ) -> 'ScrollArea':
        widget = Frame(self, f'{self.objectName()}Widget')
        layout_t = VLayout if vertical else HLayout
        layout = layout_t(widget).init()
        for item in items:
            layout.addWidget(item)
        self.setWidget(widget.init(layout=layout))
        return self
