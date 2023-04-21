from PyQt5.QtWidgets import QWidget
from contextlib import suppress as _suppress
import uuid

from ..contextapi import ui


class ContextObjectExt:
    def __init__(self, parent: QWidget = None, name: str = str(uuid.uuid4()), visible: bool = True):
        if parent and name:
            self.setObjectName(name)
            setattr(parent, name, self)
            setattr(self, parent.objectName(), parent)
            setattr(ui, name, self)

            self.core = parent
            while p := self.core.parent():
                self.core = p

        with _suppress(Exception):
            self.setVisible(visible)
