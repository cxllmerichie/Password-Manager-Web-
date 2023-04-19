from PyQt5.QtWidgets import QFrame, QWidget, QLayout

from ._wrapper import Wrapper


class Frame(Wrapper, QFrame):
    def __init__(self, parent: QWidget, name: str, visible: bool = True, stylesheet: str = None):
        QFrame.__init__(self, parent)
        Wrapper.__init__(self, parent, name, visible)
        if stylesheet:
            self.setStyleSheet(stylesheet)

    def init(
            self, *,
            layout: QLayout = None
    ) -> 'Frame':
        if layout:
            self.setLayout(layout)
        return self
