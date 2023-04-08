from PyQt5.QtWidgets import QTextEdit, QWidget


class TInput(QTextEdit):
    def __init__(self, parent: QWidget, name: str):
        super().__init__(parent)
        self.setObjectName(name)

    def init(
            self, *,
            placeholder: str = '', text: str = '',
            textchanged: callable = None
    ) -> 'TInput':
        self.setText(text)
        self.setPlaceholderText(placeholder)
        if textchanged:
            self.textChanged.connect(textchanged)
        return self
