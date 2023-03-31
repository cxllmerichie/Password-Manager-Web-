from PyQt5.QtWidgets import QLabel, QWidget
from PyQt5.QtCore import Qt, QSize


class Label(QLabel):
    def __init__(self, parent: QWidget, name: str):
        super().__init__(parent)
        self.setObjectName(name)

    async def init(
            self, *,
            text: str = '', alignment: Qt.Alignment = None, wrap: bool = False, size: QSize = None
    ) -> 'Label':
        self.setText(text)
        self.setWordWrap(wrap)
        if alignment:
            self.setAlignment(alignment)
        if size:
            self.setFixedSize(size)
        return self
