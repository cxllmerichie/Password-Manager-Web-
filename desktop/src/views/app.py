from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import QSettings, QSize

from ..css import app
from ..components import StatusBar, MenuBar, AppPages
from ..assets import Icon


class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setObjectName(self.__class__.__name__)
        self.setStyleSheet(app.css)
        self.settings = QSettings('cxllmerichie', 'PasswordManagerDesktop', self)

    async def init(self) -> 'App':
        self.resize(QSize(800, 600))
        self.setWindowTitle('Password Manager by <cxllmerichie>')
        self.setWindowIcon(QIcon(Icon.app))

        self.setCentralWidget(await AppPages(self).init())
        self.setStatusBar(await StatusBar(self).init())
        self.setMenuBar(await MenuBar(self).init())
        return self
