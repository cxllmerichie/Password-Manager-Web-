from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QPushButton, QWidget
from PyQt5.QtCore import QSize


class Button(QPushButton):
    def __init__(self, parent: QWidget, name: str):
        super().__init__(parent)
        self.setObjectName(name)

    async def init(
            self, *,
            text: str = '',
            size: QSize = None, icon: tuple[QIcon, QSize] = None,
            disabled: bool = False, slot: callable = lambda: None
    ) -> 'Button':
        self.setText(text)
        self.clicked.connect(slot)
        if size:
            self.setFixedSize(size)
        if icon:
            self.setIcon(QIcon(icon[0]))
            self.setIconSize(icon[1])
        self.setDisabled(disabled)
        return self
