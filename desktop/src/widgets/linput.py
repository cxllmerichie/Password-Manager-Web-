from PyQt5.QtWidgets import QLineEdit, QWidget
from PyQt5.QtCore import Qt


class LInput(QLineEdit):
    def __init__(self, parent: QWidget, name: str):
        super().__init__(parent)
        self.setObjectName(name)

    def init(
            self, *,
            placeholder: str = '', text: str = '', hidden: bool = False,
            textchanged: callable = None, alignment: Qt.Alignment = None
    ) -> 'LInput':
        self.setText(text)
        self.setPlaceholderText(placeholder)
        if hidden:
            self.setEchoMode(QLineEdit.Password)
        if textchanged:
            self.textChanged.connect(textchanged)
        if alignment:
            self.setAlignment(alignment)
        return self

    def hide_echo(self):
        self.setEchoMode(QLineEdit.Password)

    def show_echo(self):
        self.setEchoMode(QLineEdit.Normal)

    def toggle_echo(self):
        self.hide_echo() if self.echoMode() == QLineEdit.Normal else self.show_echo()
