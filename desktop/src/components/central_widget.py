from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt

from ..widgets import StackedWidget, ui
from .view_signin import SignIn
from .view_signup import SignUp
from .view_main import MainView


class CentralWidget(StackedWidget):
    def __init__(self, parent: QWidget):
        super().__init__(parent, self.__class__.__name__)

    def init(self) -> 'CentralWidget':
        self.layout().setAlignment(Qt.AlignHCenter)
        self.addWidget(SignIn(self).init())
        self.addWidget(SignUp(self).init())
        # ui.token = None
        if not ui.token:
            self.setCurrentWidget(self.SignIn)
        else:
            self.addWidget(widget := MainView(self).init())
            self.setCurrentWidget(widget)
        return self
