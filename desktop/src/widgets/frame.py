from PyQt5.QtWidgets import QFrame, QWidget, QLayout
import uuid

from ._wrapper import Wrapper


class Frame(QFrame, Wrapper):
    def __init__(self, parent: QWidget, name: str = str(uuid.uuid4()), visible: bool = True):
        QFrame.__init__(self, parent)
        Wrapper.__init__(self, parent, name, visible)

    def init(
            self, *,
            layout: QLayout = None
    ) -> 'Frame':
        if layout:
            self.setLayout(layout)
        return self
