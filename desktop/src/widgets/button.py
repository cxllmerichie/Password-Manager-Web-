from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QPushButton, QWidget
from PyQt5.QtCore import QSize

from ..misc import Icon
from ._wrapper import Wrapper


class Button(QPushButton, Wrapper):
    def __init__(self, parent: QWidget, name: str, visible: bool = True):
        QPushButton.__init__(self, parent)
        Wrapper.__init__(self, parent, name, visible)

    def init(
            self, *,
            text: str = '',
            size: QSize = None, icon: Icon = None,
            disabled: bool = False, slot: callable = lambda: None
    ) -> 'Button':
        self.setText(text)
        self.setDisabled(disabled)
        self.clicked.connect(slot)
        if size:
            self.setFixedSize(size)
        if icon:
            self.setIcon(QIcon(icon.icon))
            self.setIconSize(icon.size)
        return self
