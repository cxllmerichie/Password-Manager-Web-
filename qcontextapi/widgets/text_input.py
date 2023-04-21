from PyQt5.QtWidgets import QTextEdit, QWidget

from ..extensions import ContextObjectExt


class TextInput(ContextObjectExt, QTextEdit):
    def __init__(self, parent: QWidget, name: str, visible: bool = True):
        QTextEdit.__init__(self, parent)
        ContextObjectExt.__init__(self, parent, name, visible)

    def init(
            self, *,
            placeholder: str = '', text: str = '', textchanged: callable = None
    ) -> 'TextInput':
        self.setText(text)
        self.setPlaceholderText(placeholder)
        if textchanged:
            self.textChanged.connect(textchanged)
        return self
