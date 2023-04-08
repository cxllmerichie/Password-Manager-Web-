from PyQt5.QtWidgets import QScrollArea, QWidget
from PyQt5.QtCore import Qt

from ..widgets import Frame
from ..widgets._layout import Layout


class ScrollArea(QScrollArea):
    def __init__(self, parent: QWidget, name: str, horizontal: bool = True, vertical: bool = True):
        super().__init__(parent)
        self.setObjectName(name)
        if not horizontal:
            self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        if not vertical:
            self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setWidgetResizable(True)

    def init(
            self, *,
            layout_t: type[Layout],
            margins: tuple[int, ...] = (0, 0, 0, 0), spacing: int = 0, alignment: Qt.Alignment = None
    ) -> 'ScrollArea':
        widget = Frame(self, f'{self.objectName()}Widget')
        layout = layout_t(widget, f'{self.objectName()}WidgetLayout').init(
            margins=margins, spacing=spacing, alignment=alignment
        )
        self.setWidget(widget.init(layout=layout))
        return self

    def clear(self):
        layout = self.widget().layout()
        for i in range(layout.count()):
            item = layout.itemAt(i)
            layout.removeItem(item)
            item.deleteLater()
