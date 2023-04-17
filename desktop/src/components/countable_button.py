from PyQt5.QtWidgets import QWidget, QPushButton
from PyQt5.QtCore import Qt

from ..widgets import Button, Label, Layout
from ..misc import Icon


class CountableButton(QPushButton):
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self.setObjectName(self.__class__.__name__)

    def init(
            self, *,
            icon: Icon, text: str, total: int,
            alignment: Qt.Alignment = None, slot: callable = lambda: None
    ) -> 'CountableButton':
        self.setLayout(Layout.horizontal().init(
            margins=(10, 0, 0, 0), spacing=10, alignment=Qt.AlignLeft,
            items=[
                Button(self, 'CountableButtonIcon').init(
                    size=icon.size, icon=icon, disabled=True
                ),
                Label(self, 'CountableButtonLbl').init(
                    text=text, alignment=alignment, elided=True
                ),
                Label(self, 'CountableButtonCountLbl').init(
                    text=str(total)
                ), Qt.AlignRight
            ]
        ))
        self.clicked.connect(slot)
        return self
