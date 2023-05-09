from PyQt5.QtWidgets import QMainWindow
from qcontextapi import CONTEXT
from PyQt5.QtCore import Qt


class App(QMainWindow):
    # all imports must be placed only in the class, otherwise `Process finished with exit code -1073740791 (0xC0000409)`
    # issue: while running (init load) it sees the import and usage from PyQt5 in `assets`, and PyQt5 itself conflicts
    # with main created thread in `main.py` creating more threads in `assets`

    def __init__(self):
        from . import stylesheets

        super().__init__()
        self.setObjectName(self.__class__.__name__)
        self.setStyleSheet(stylesheets.app.css +
                           stylesheets.status_bar.css)

    def init(self) -> 'App':
        from .misc import SIZES

        self.resize(SIZES.App)
        self.setWindowFlag(Qt.FramelessWindowHint)
        if not CONTEXT['storage']:
            from .components import FullscreenPopup

            fspopup = FullscreenPopup(self).init()
        else:
            from .views.central_widget import CentralWidget
            from desktop.src.components.status_bar import StatusBar

            statusbar = StatusBar(self).init()
            self.setCentralWidget(CentralWidget(self).init())
            self.setStatusBar(statusbar)
            statusbar.post_init()
        return self
