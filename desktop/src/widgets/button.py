from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QPushButton, QWidget
from PyQt5.QtCore import QSize

from ..const import Icon


class Button(QPushButton):
    def __init__(self, parent: QWidget, name: str):
        super().__init__(parent)
        self.setObjectName(name)

    async def init(
            self, *,
            text: str = '',
            size: QSize = None, icon: Icon = None,
            disabled: bool = False, slot: callable = lambda: None
    ) -> 'Button':
        self.setText(text)
        self.clicked.connect(slot)
        if size:
            self.setFixedSize(size)
        if icon:
            self.setIcon(QIcon(icon.icon))
            self.setIconSize(icon.size)
        self.setDisabled(disabled)
        return self
