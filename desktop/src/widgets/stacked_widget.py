from PyQt5.QtWidgets import QWidget, QStackedWidget

from ._wrapper import Wrapper


class StackedWidget(Wrapper, QStackedWidget):
    def __init__(self, parent: QWidget, name: str, visible: bool = True, stylesheet: str = None):
        QStackedWidget.__init__(self, parent)
        Wrapper.__init__(self, parent, name, visible)
        if stylesheet:
            self.setStyleSheet(stylesheet)

        self.addWidget(QWidget(self))

    def setCurrentIndex(self, index: int) -> None:
        super().setCurrentIndex(index + 1)
