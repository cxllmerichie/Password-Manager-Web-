from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon
import os


class Icon:
    def __init__(self, filename: str, size: tuple[int, int]):
        self.icon: QIcon = QIcon(self.path(filename))
        self.size: QSize = QSize(*size)

    @staticmethod
    def path(filename: str) -> str:
        return os.path.join(os.path.abspath('.assets'), 'icons', filename)


class Icons:
    APP = Icon('icon.png', (25, 25))
    MINIMIZE = Icon('minus.svg', (25, 25))
    RESTORE = Icon('square.svg', (20, 20))
    CROSS = Icon('x.svg', (27, 27))
    HOME = Icon('home.svg', (20, 20))
    FAVOURITE = Icon('star.svg', (20, 20))
    MENU = Icon('menu.svg', (25, 25))
