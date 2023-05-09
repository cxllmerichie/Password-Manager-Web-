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
        self.loaded: bool = False
        self.currentChanged.connect(self.current_widget_changed)

    def init(self) -> 'CentralWidget':
        self.layout().setAlignment(Qt.AlignHCenter)
        self.addWidget(SignIn(self).init())
        self.addWidget(SignUp(self).init())
        self.addWidget(MainView(self))
        # enum comparison gives invalid result, so comparing values (reason: QObject.setProperty() uses `pickle`)
        if CONTEXT['storage'].value is utils.Storage.LOCAL.value or not utils.is_connected() or CONTEXT['token']:
            self.setCurrentWidget(CONTEXT.MainView)
        else:
            self.setCurrentWidget(CONTEXT.SignIn)
        return self

    def current_widget_changed(self):
        CONTEXT.LogoutBtn.setVisible(CONTEXT['token'] is not None)
        if self.currentWidget().objectName() == 'MainView':
            if not self.loaded:
                self.currentWidget().init()
                self.loaded = True
