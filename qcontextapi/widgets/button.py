from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QPushButton, QWidget, QSizePolicy
from PyQt5.QtCore import QSize
from contextlib import suppress

from ..utils import Icon
from ..extensions import ContextObjectExt


class Button(ContextObjectExt, QPushButton):
    slot: callable

    def __init__(self, parent: QWidget, name: str, visible: bool = True):
        QPushButton.__init__(self, parent)
        ContextObjectExt.__init__(self, parent, name, visible)

    def init(
            self, *,
            text: str = '', size: QSize = None, icon: Icon = None,
            disabled: bool = False, slot: callable = lambda: None, policy: tuple[QSizePolicy, QSizePolicy] = None
    ) -> 'Button':
        self.slot = slot
        self.setText(text)
        self.setDisabled(disabled)
        self.clicked.connect(slot)
        if size:
            self.setFixedSize(size)
        if icon:
            self.setIcon(QIcon(icon.icon))
            self.setIconSize(icon.size)
        if policy:
            self.setSizePolicy(*policy)
        return self

    # def setDisabled(self, disabled: bool) -> None:
    #     # super().setDisabled(disabled)
    #     self.__toggle_disable(not disabled)
    #
    # def setEnabled(self, enabled: bool) -> None:
    #     # super().setEnabled(enabled)
    #     self.__toggle_disable(enabled)
    #
    # def __toggle_disable(self, enabled: bool):
    #     if enabled:
    #         self.clicked.connect(self.slot)
    #     else:
    #         with suppress(Exception):
    #             self.clicked.disconnect()
