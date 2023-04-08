from PyQt5.QtWidgets import QVBoxLayout, QWidget
from PyQt5.QtCore import Qt

from ._layout import Layout


class VLayout(QVBoxLayout, Layout):
    def __init__(self, parent: QWidget = None, name: str = None):
        super().__init__(parent)
        if name:
            self.setObjectName(name)

    def init(
            self, *,
            margins: tuple[int, ...] = (0, 0, 0, 0), spacing: int = 0, alignment: Qt.Alignment = None,
            items: list[QWidget] = None
    ) -> 'VLayout':
        Layout.init(self, margins=margins, spacing=spacing, alignment=alignment)
        return self
