from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QPushButton, QWidget
from PyQt5.QtCore import QSize, pyqtSlot
from threading import Thread
from typing import Coroutine, Awaitable, Callable
import asyncio

from ..misc import Icon


class Button(QPushButton):
    def __init__(self, parent: QWidget, name: str):
        super().__init__(parent)
        self.setObjectName(name)

    @staticmethod
    @pyqtSlot()
    def emit(slot: Awaitable | Callable) -> callable:
        if isinstance(result := slot(), Coroutine):
            asyncio.ensure_future(result)
            # return Thread(target=asyncio.new_event_loop().run_until_complete, args=(result,)).start()
        return result

    async def init(
            self, *,
            text: str = '',
            size: QSize = None, icon: Icon = None,
            disabled: bool = False, slot: callable = lambda: None
    ) -> 'Button':
        self.setText(text)
        self.setDisabled(disabled)
        self.clicked.connect(lambda: self.emit(slot))
        if size:
            self.setFixedSize(size)
        if icon:
            self.setIcon(QIcon(icon.icon))
            self.setIconSize(icon.size)
        return self
