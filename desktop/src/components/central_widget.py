from PyQt5.QtWidgets import QStackedWidget, QWidget
from PyQt5.QtCore import Qt

from .sign_in import SignIn
from .sign_up import SignUp
from .main_view import MainView


class CentralWidget(QStackedWidget):
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self.setObjectName(self.__class__.__name__)

    def init(self) -> 'CentralWidget':
        self.layout().setAlignment(Qt.AlignHCenter)
        self.addWidget(SignIn(self).init())
        self.addWidget(SignUp(self).init())
        self.parent().settings.setValue('token', None)
        if not self.parent().token():
            self.setCurrentIndex(0)
        else:
            self.addWidget(MainView(self).init())
            self.setCurrentIndex(2)
        return self
