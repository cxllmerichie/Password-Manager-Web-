from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QPushButton, QWidget
from PyQt5.QtCore import QSize


class Button(QPushButton):
    def __init__(self, parent: QWidget):
        super().__init__(parent)

    async def init(self,
                   text: str, name: str, signal: callable = lambda: None,
                   *, icon: str = None, isize: QSize = QSize(25, 25)) -> 'Button':
        self.setText(text)
        self.setObjectName(name)
        self.clicked.connect(signal)
        if icon:
            self.setIcon(QIcon(icon))
            self.setIconSize(isize)
        return self
