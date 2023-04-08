from typing import Iterable
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QIcon, QImage, QPixmap
import os
import base64


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
    EDIT = Icon('edit.svg', (30, 30))
    CROSS_CIRCLE = Icon('x-circle.svg', (20, 20))
    COPY = Icon('copy.svg', (20, 20))
    EYE = Icon('eye.svg', (20, 20))
    EYE_OFF = Icon('eye-off.svg', (20, 20))

    @staticmethod
    def from_bytes(icon_bytes: bytes | str) -> QIcon:
        if isinstance(icon_bytes, str):
            icon_bytes = eval(icon_bytes)
        pixmap = QPixmap()
        png = base64.b64encode(icon_bytes).decode('utf-8')
        pixmap.loadFromData(base64.b64decode(png))
        return QIcon(pixmap)
