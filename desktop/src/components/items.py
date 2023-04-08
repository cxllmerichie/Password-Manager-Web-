from PyQt5.QtWidgets import QWidget

from ..widgets import ScrollArea
from ..css import items


class Items(ScrollArea):
    def __init__(self, parent: QWidget):
        super().__init__(parent, 'Items')
        self.setStyleSheet(items.css)
