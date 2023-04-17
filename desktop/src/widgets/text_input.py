from PyQt5.QtWidgets import QTextEdit, QWidget


class TextInput(QTextEdit):
    def __init__(self, parent: QWidget, name: str):
        super().__init__(parent)
        self.setObjectName(name)

    def init(
            self, *,
            placeholder: str = '', text: str = '',
            textchanged: callable = None
    ) -> 'TextInput':
        self.setText(text)
        self.setPlaceholderText(placeholder)
        if textchanged:
            self.textChanged.connect(textchanged)
        return self
