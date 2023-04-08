from PyQt5.QtWidgets import QLineEdit, QWidget


class LInput(QLineEdit):
    def __init__(self, parent: QWidget, name: str):
        super().__init__(parent)
        self.setObjectName(name)

    def init(
            self, *,
            placeholder: str = '', text: str = '', hidden: bool = False,
            textchanged: callable = None
    ) -> 'LInput':
        self.setText(text)
        self.setPlaceholderText(placeholder)
        if hidden:
            self.setEchoMode(QLineEdit.Password)
        if textchanged:
            self.textChanged.connect(textchanged)
        return self
