from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtCore import Qt


class VBox(QVBoxLayout):
    def __init__(self, parent=None):
        super().__init__(parent)

    async def init(
            self,
            margins: tuple[int, ...] = (0, 0, 0, 0),
            spacing: int = 0, alignment: Qt.Alignment = Qt.AlignVCenter | Qt.AlignHCenter
    ) -> 'VBox':
        self.setContentsMargins(*margins)
        self.setSpacing(spacing)
        self.setAlignment(alignment)
        return self
