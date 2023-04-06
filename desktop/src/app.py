from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import QSettings
from PyQt5.QtCore import Qt


class App(QMainWindow):
    # all imports must be placed only in the class, otherwise `Process finished with exit code -1073740791 (0xC0000409)`
    # issue: while running (init load) it sees the import and usage from PyQt5 in `assets`, and PyQt5 itself conflicts
    # with main created thread in `main.py` creating more threads in `assets`

    def __init__(self):
        from .css import app, status_bar

        super().__init__()
        self.setObjectName(self.__class__.__name__)
        self.setStyleSheet(app.css + status_bar.css)
        self.settings = QSettings('cxllmerichie', 'PasswordManagerDesktop', self)

    async def init(self) -> 'App':
        from .misc import Sizes
        from .views.main_view import CentralWidget
        from .components import StatusBar

        self.resize(Sizes.App)
        self.setWindowFlag(Qt.FramelessWindowHint)
        # self.setWindowIcon(Icons.APP.icon)

        # self.setMenuBar(await MenuBar(self).init())
        self.setCentralWidget(await CentralWidget(self).init())
        self.setStatusBar(await StatusBar(self).init())
        return self
