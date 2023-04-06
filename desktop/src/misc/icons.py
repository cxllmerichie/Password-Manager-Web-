from typing import Iterable
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon, QImage, QPixmap
import os


class Icon:
    def __init__(self, filename: str, size: tuple[int, int]):
        self.icon: QIcon = QIcon(self.path(filename))
        self.size: QSize = QSize(*size)

    @staticmethod
    def path(filename: str, root: str = '.assets', middleware: Iterable[str] = ('icons', )) -> str:
        return os.path.join(os.path.abspath(root), *middleware, filename)

    def adjusted(self, filename: str = None, size: tuple[int, int] = None) -> 'Icon':
        if filename:
            self.icon = QIcon(self.path(filename))
        if size:
            self.size = QSize(*size)
        return self


class Icons:
    APP = Icon('icon.png', (25, 25))
    MINIMIZE = Icon('minus.svg', (25, 25))
    RESTORE = Icon('square.svg', (20, 20))
    CROSS = Icon('x.svg', (27, 27))
    HOME = Icon('home.svg', (20, 20))
    STAR = Icon('star.svg', (20, 20))
    STAR_FILL = Icon('star-fill.svg', (20, 20))
    MENU = Icon('menu.svg', (25, 25))
    PLUS = Icon('plus-circle.svg', (20, 20))
    CATEGORY = Icon('tag.svg', (80, 80))

    @staticmethod
    def from_bytes(icon_bytes: bytes = None) -> QIcon:
        qimg = QImage.fromData(icon_bytes, 'PNG')
        qpix = QPixmap.fromImage(qimg)
        return QIcon(qpix)
