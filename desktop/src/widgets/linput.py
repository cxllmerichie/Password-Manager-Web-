from PyQt5.QtWidgets import QLineEdit, QWidget


class LInput(QLineEdit):
    def __init__(self, parent: QWidget):
        super().__init__(parent)

    async def init(self, placeholder: str, name: str, *, text: str = '', password: bool = False) -> 'LInput':
        self.setText(text)
        self.setPlaceholderText(placeholder)
        self.setObjectName(name)
        if password:
            self.setEchoMode(QLineEdit.Password)
        return self
