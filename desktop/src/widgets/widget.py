from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt

from ._wrapper import Wrapper


class Widget(Wrapper, QWidget):
    def __init__(self, parent: QWidget, name: str, visible: bool = True, stylesheet: str = None):
        QWidget.__init__(self, parent)
        Wrapper.__init__(self, parent, name, visible)
        if stylesheet:
            self.setAttribute(Qt.WA_StyledBackground, True)
            self.setStyleSheet(stylesheet)
