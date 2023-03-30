from PyQt5.QtWidgets import QLabel, QWidget
from PyQt5.QtCore import Qt


class Label(QLabel):
    def __init__(self, parent: QWidget, name: str):
        super().__init__(parent)
        self.setObjectName(name)

    async def init(
            self, *,
            text: str, alignment: Qt.Alignment = None
    ) -> 'Label':
        self.setText(text)
        if alignment:
            self.setAlignment(alignment)
        return self
