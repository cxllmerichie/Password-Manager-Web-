from PyQt5.QtWidgets import QWidget, QCompleter
from PyQt5.QtCore import Qt
from typing import Iterable

from ..widgets import LineInput


class SearchBar(LineInput):
    def __init__(self, parent: QWidget, name: str = None):
        LineInput.__init__(self, parent, name if name else self.__class__.__name__, True)

    def init(self, items: Iterable[str], update: callable, placeholder: str = '') -> 'SearchBar':
        completer = QCompleter(items)
        completer.setCaseSensitivity(Qt.CaseInsensitive)
        completer.popup().setObjectName(f'{self.objectName()}Popup')
        self.setCompleter(completer)
        super().init(textchanged=update, placeholder=placeholder)
        return self
