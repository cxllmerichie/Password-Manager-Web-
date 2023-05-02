from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QPushButton, QWidget, QSizePolicy
from PyQt5.QtCore import QSize
from typing import Callable, Any
from contextlib import suppress

from ..misc import Icon
from ..extensions import ContextObjectExt


class Button(ContextObjectExt, QPushButton):
    def __init__(self, parent: QWidget, name: str, visible: bool = True):
        QPushButton.__init__(self, parent)
        ContextObjectExt.__init__(self, parent, name, visible)

    def init(
            self, *,
            text: str = '', size: QSize = None, icon: Icon = None, disabled: bool = False,
            slot: Callable[..., Any] = lambda: None, policy: tuple[QSizePolicy, QSizePolicy] = None
    ) -> 'Button':
        self.setText(text)
        self.setDisabled(disabled)

        with suppress(Exception):
            self.clicked.disconnect()
        self.clicked.connect(slot)

        if size:
            self.setFixedSize(size)
        if icon:
            self.setIcon(QIcon(icon.icon))
            self.setIconSize(icon.size)
        if policy:
            self.setSizePolicy(*policy)
        return self
