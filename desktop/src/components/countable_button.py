from PyQt5.QtWidgets import QWidget, QPushButton
from PyQt5.QtCore import Qt
from typing import Any

from ..widgets import Button, Label, HLayout
from ..misc import Icon


class CountableButton(QPushButton):
    def __init__(self, parent: QWidget, name: str = None):
        super().__init__(parent)
        self.setObjectName(self.__class__.__name__)
        if name:
            self.setObjectName(name)

    async def init(
            self, *,
            icon: Icon, text, total: int | list[Any, ...],
            alignment: Qt.Alignment = None, slot: callable = lambda: None
    ) -> 'CountableButton':
        layout = await HLayout().init(margins=(10, 0, 0, 0), spacing=10, alignment=Qt.AlignLeft)
        layout.addWidget(await Button(self, 'CountableButtonIcon').init(
            size=icon.size, icon=icon, disabled=True
        ))
        layout.addWidget(await Label(self, 'CountableButtonLbl').init(
            text=text, alignment=alignment
        ))
        layout.addWidget(await Label(self, 'CountableButtonCountLbl').init(
            text=str(total) if isinstance(total, int) else str(len(total))
        ), alignment=Qt.AlignRight)
        self.setLayout(layout)
        self.clicked.connect(slot)
        return self
