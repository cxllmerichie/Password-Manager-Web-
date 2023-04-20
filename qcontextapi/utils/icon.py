from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import QSize
from typing import Iterable
import base64
import os


class Icon:
    root = '../qcontextapi/assets'

    def __init__(self, filename: str, size: tuple[int, int], icon: QIcon = None):
        if isinstance(filename, str):
            if not os.path.exists(filepath := self.path(filename)):
                raise FileNotFoundError(f'file: {filename} not found for `Icon`')
            self.icon = QIcon(filepath)
        else:
            self.icon = icon
        if isinstance(size, tuple):
            self.size: QSize = QSize(*size)

    @staticmethod
    def path(filename: str, root: str = '.assets', middleware: Iterable[str] = ('icons', )) -> str:
        return os.path.join(os.path.abspath(root), *middleware, filename)

    def adjusted(self, filename: str = None, size: tuple[int, int] | QSize = None) -> 'Icon':
        if filename:
            self.icon = QIcon(self.path(filename))
        if size:
            self.size = QSize(*size) if isinstance(size, tuple) else size
        return self

    @staticmethod
    def from_bytes(icon_bytes: bytes | str) -> 'Icon':
        if isinstance(icon_bytes, str):
            icon_bytes = eval(icon_bytes)
        pixmap = QPixmap()
        png = base64.b64encode(icon_bytes).decode('utf-8')
        pixmap.loadFromData(base64.b64decode(png))
        return Icon(..., ..., QIcon(pixmap))
