from PyQt5.QtWidgets import QSplitter


class SplitterWidget:
    splitter: QSplitter
    expand_to: int

    def _index(self) -> int:
        for index in range(self.splitter.count()):
            if self == self.splitter.widget(index):
                return index
        raise IndexError(f'{self} not found in {self.splitter} widgets')

    def _set_size(self, size: int):
        index = self._index()
        self.splitter.setSizes([*self.splitter.sizes()[:index], size, *self.splitter.sizes()[index + 1:]])

    def expand(self, size: int = None):
        size = size if size else self.expand_to
        self._set_size(size)

    def shrink(self) -> None:
        self._set_size(0)

    def toggle(self) -> None:
        if self.splitter.sizes()[self._index()] > 0:
            self._set_size(0)
        else:
            self._set_size(self.expand_to)
