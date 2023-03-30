from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import QSettings, QSize, Qt

from .css import app
from .components import StatusBar, MenuBar
from .views.main_view import CentralWidget
from .assets import Icons, Sizes


class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setObjectName(self.__class__.__name__)
        self.setStyleSheet(app.css)
        self.settings = QSettings(organization='cxllmerichie', application='PasswordManagerDesktop', parent=self)

    async def init(self) -> 'App':
        self.resize(Sizes.App)
        self.setWindowFlag(Qt.FramelessWindowHint)
        # self.setWindowTitle('Password Manager by <cxllmerichie>')
        # self.setWindowIcon(Icons.APP.icon)

        self.setCentralWidget(await CentralWidget(self).init())
        # self.setStatusBar(await StatusBar(self).init())
        # self.setMenuBar(await MenuBar(self).init())
        return self
