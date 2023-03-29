from PyQt5.QtWidgets import QLabel, QWidget


class Label(QLabel):
    def __init__(self, parent: QWidget):
        super().__init__(parent)

    async def init(self, text: str, name: str = None) -> 'Label':
        self.setText(text)
        self.setObjectName(name)
        return self
