from PyQt5.QtWidgets import QWidget, QPushButton
from PyQt5.QtCore import Qt
from typing import Any

from ..widgets import Button, Label, HLayout
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
        layout = HLayout().init(margins=(10, 0, 0, 0), spacing=10, alignment=Qt.AlignLeft)
        layout.addWidget(Button(self, 'CountableButtonIcon').init(
            size=icon.size, icon=icon, disabled=True
        ))
        layout.addWidget(Label(self, 'CountableButtonLbl').init(
            text=text, alignment=alignment, elided=True
        ))
        layout.addWidget(Label(self, 'CountableButtonCountLbl').init(
            text=str(total)
        ), alignment=Qt.AlignRight)
        self.setLayout(layout)
        self.clicked.connect(slot)
        return self
