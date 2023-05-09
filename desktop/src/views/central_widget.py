from qcontextapi.widgets import StackedWidget
from qcontextapi import CONTEXT
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt

from .view_signin import SignIn
from .view_signup import SignUp
from .view_main import MainView
from ..misc import utils


class CentralWidget(StackedWidget):
    def __init__(self, parent: QWidget):
        super().__init__(parent, self.__class__.__name__)

    def init(self) -> 'CentralWidget':
        self.layout().setAlignment(Qt.AlignHCenter)
        self.addWidget(SignIn(self).init())
        self.addWidget(SignUp(self).init())
        # CONTEXT['token'] = None
        if CONTEXT['storage'] == utils.Storage.LOCAL or CONTEXT['token'] or not utils.is_connected():
            self.addWidget(widget := MainView(self).init())
            self.setCurrentWidget(widget)
        else:
            self.setCurrentWidget(CONTEXT.SignIn)
        return self
