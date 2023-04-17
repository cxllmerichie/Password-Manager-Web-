from PyQt5.QtWidgets import QFrame, QWidget, QLayout

from ._wrapper import Wrapper


class Frame(Wrapper, QFrame):
    def __init__(self, parent: QWidget, name: str = None, visible: bool = True):
        QFrame.__init__(self, parent)
        Wrapper.__init__(self, parent, name, visible)

    def init(
            self, *,
            layout: QLayout = None
    ) -> 'Frame':
        if layout:
            self.setLayout(layout)
        return self
