from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon
import os


class Icon:
    def __init__(self, filename: str, size: tuple[int, int]):
        self.icon: QIcon = QIcon(self.path(filename))
        self.size: QSize = QSize(*size)

    @staticmethod
    def path(filename: str) -> str:
        return os.path.join(os.path.abspath('src'), 'assets', 'icons', filename)


class Icons:
    APP = Icon('icon.png', (40, 40))
    MINIMIZE = Icon('minus.svg', (40, 40))
    RESTORE = Icon('square.svg', (40, 40))
    CROSS = Icon('x.svg', (40, 40))
    HOME = Icon('home.svg', (25, 25))
    FAVOURITE = Icon('star.svg', (25, 25))
    MENU = Icon('menu.svg', (40, 40))
