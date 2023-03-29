from PyQt5.QtWidgets import QPushButton, QWidget


class Button(QPushButton):
    def __init__(self, parent: QWidget):
        super().__init__(parent)

    async def init(self, text: str, name: str, signal: callable = lambda: None) -> 'Button':
        self.setText(text)
        self.setObjectName(name)
        self.clicked.connect(signal)
        return self
