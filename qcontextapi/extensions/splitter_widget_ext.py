from PyQt5.QtWidgets import QSplitter
from PyQt5.QtCore import Qt

from loguru import logger as _logger


class SplitterWidgetExt:
    splitter: QSplitter

    def __init__(self, expand_to: int, *,
                 expand_min: int = None, expand_max: int = None, orientation: Qt.Orientation = None):
        self.expand_to: int = expand_to

        if expand_min or expand_max:
            if not orientation:
                _logger.info('`expand_min` and `expand_max` set but `orientation` is `None`')
            dimension = 'width' if orientation is Qt.Horizontal else 'height'
            if expand_min:
                getattr(self, f'setMin{dimension.capitalize()}')(expand_min)
            if expand_max:
                getattr(self, f'setMax{dimension.capitalize()}')(expand_max)

    def _index(self) -> int:
        for index in range(self.splitter.count()):
            if self == self.splitter.widget(index):
                return index
        raise IndexError(f'{self} not found in {self.splitter} widgets')

    def _set_size(self, size: int):
        index = self._index()
        self.splitter.setSizes([*self.splitter.sizes()[:index], size, *self.splitter.sizes()[index + 1:]])

    def expand(self, size: int = None):
        if not self.splitter.sizes()[self._index()]:
            self._set_size(size if size else self.expand_to)

    def shrink(self) -> None:
        self._set_size(0)

    def toggle(self) -> None:
        if self.splitter.sizes()[self._index()]:
            self.shrink()
        else:
            self.expand()
