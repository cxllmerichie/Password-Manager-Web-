from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import QSize
import base64
import os
from loguru import logger

from .size import Size


class Icon:
    IconType = type[QIcon, str, bytes]
    SizeType = type[Size, QSize, tuple[int, int], Ellipsis, None]

    root = '../qcontextapi/.assets'
    __icon: QIcon = None
    __size: QSize = None

    def __init__(self, instance: IconType, size: SizeType = None):
        self.icon = instance
        if size:
            self.size = size

    @property
    def icon(self) -> QIcon:
        return self.__icon

    @property
    def size(self) -> QSize:
        return self.__size

    @icon.setter
    def icon(self, instance: IconType) -> None:
        """

        :param instance: QIcon, string filename with already set Icon.root, icon bytes
        :return:
        """
        def from_bytes(icon_bytes: bytes):
            pixmap = QPixmap()
            png = base64.b64encode(icon_bytes).decode('utf-8')
            pixmap.loadFromData(base64.b64decode(png))
            self.__icon = QIcon(pixmap)

        if isinstance(instance, QIcon):
            self.__icon = instance
        elif isinstance(instance, str):
            if os.path.exists(filepath := os.path.join(os.path.abspath(self.root), instance)):
                self.__icon = QIcon(filepath)
            elif isinstance((icon_bytes := eval(instance)), bytes):
                from_bytes(icon_bytes)
            else:
                raise FileNotFoundError(f'file: {filepath} not found for `Icon`')
        elif isinstance(instance, bytes):
            from_bytes(instance)
        else:
            raise AttributeError(f'unknown type ({type(instance)}) of instance ({instance}), can not set Icon.icon')

    @size.setter
    def size(self, size: SizeType) -> None:
        """

        :param size: QSize, qcontextapi.Size, tuple[int, int]
        :return:
        """
        if isinstance(size, tuple):
            self.__size = QSize(*size)
        elif isinstance(size, Size):
            self.__size = QSize(*size.size)
        elif isinstance(size, QSize):
            self.__size = size
        else:
            raise AttributeError(f'unknown type ({type(size)}) of size ({size}), can not set Icon.size')

    def adjusted(self, instance: IconType = None, size: SizeType = None) -> 'Icon':
        if not instance and not size:
            logger.warning('Icon.adjusted() called without parameters. Redundant call.')
        if instance:
            self.icon = instance
        if size:
            self.size = size
        return self
