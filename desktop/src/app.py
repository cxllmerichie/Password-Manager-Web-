from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import QSettings
from PyQt5.QtCore import Qt

from .css import app


class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setObjectName(self.__class__.__name__)
        self.setStyleSheet(app.css)
        self.settings = QSettings('cxllmerichie', 'PasswordManagerDesktop', self)

    async def init(self) -> 'App':
        # both imports must be placed exactly here, otherwise `Process finished with exit code -1073740791 (0xC0000409)`
        # issue: while indexing it sees the import and usage from PyQt5 in `assets`, and PyQt5 itself conflicts
        # with another created thread in `main.py` creating another thread in `assets`
        from .assets import Sizes
        from .views.main_view import CentralWidget
        from .components import StatusBar, MenuBar

        self.resize(Sizes.App)
        self.setWindowFlag(Qt.FramelessWindowHint)
        # self.setWindowTitle('Password Manager by <cxllmerichie>')
        # self.setWindowIcon(Icons.APP.icon)

        self.setCentralWidget(await CentralWidget(self).init())
        # self.setStatusBar(await StatusBar(self).init())
        # self.setMenuBar(await MenuBar(self).init())
        return self
