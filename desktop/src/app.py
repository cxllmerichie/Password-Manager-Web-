from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import Qt
from qcontextapi import CONTEXT


class App(QMainWindow):
    # all imports must be placed only in the class, otherwise `Process finished with exit code -1073740791 (0xC0000409)`
    # issue: while running (init load) it sees the import and usage from PyQt5 in `assets`, and PyQt5 itself conflicts
    # with main created thread in `main.py` creating more threads in `assets`

    def __init__(self):
        from . import css

        super().__init__()
        self.setObjectName(self.__class__.__name__)
        self.setStyleSheet(css.app.css + css.status_bar.css)

    def init(self) -> 'App':
        from .misc import SIZES

        self.resize(SIZES.App)
        self.setWindowFlag(Qt.FramelessWindowHint)
        CONTEXT['local'] = False
        CONTEXT['storage'] = None
        if not CONTEXT['storage']:
            from .components import FullscreenPopup

            fspopup = FullscreenPopup(self).init()
        else:
            from .views.central_widget import CentralWidget
            from desktop.src.components.status_bar import StatusBar
            from .misc import utils

            self.setCentralWidget(CentralWidget(self).init())
            self.setStatusBar(StatusBar(self).init())
            if CONTEXT['local']:
                utils.start_local()
        return self
