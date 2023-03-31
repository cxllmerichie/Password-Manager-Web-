from PyQt5.QtWidgets import QStackedWidget, QWidget, QHBoxLayout, QFrame
from PyQt5.QtCore import Qt

from .sign_in import SignIn
from .sign_up import SignUp
from ..widgets import VLayout, HLayout, Frame
from ..components import LeftMenu, RightPages, CenterPages, Panel


class CentralWidget(QStackedWidget):
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self.setObjectName(self.__class__.__name__)

    async def init(self) -> 'CentralWidget':
        self.layout().setAlignment(Qt.AlignHCenter)
        self.addWidget(await SignIn(self).init())
        self.addWidget(await SignUp(self).init())
        self.addWidget(await MainView(self).init())
        if not self.parent().settings.value('access_token'):
            self.setCurrentIndex(2)
        else:
            self.setCurrentIndex(2)
        return self


class MainView(QWidget):
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self.setObjectName(self.__class__.__name__)

    async def init(self) -> 'MainView':
        vbox = await VLayout().init()
        vbox.addWidget(await Panel(self).init(), alignment=Qt.AlignTop)

        hbox = await HLayout(self).init()
        hbox.addWidget(await LeftMenu(self, 220).init())
        hbox.addWidget(await CenterPages(self).init())
        hbox.addWidget(await RightPages(self, 200).init())
        vbox.addWidget(await Frame(self, 'AppViewFrame').init(layout=hbox))

        self.setLayout(vbox)
        return self
