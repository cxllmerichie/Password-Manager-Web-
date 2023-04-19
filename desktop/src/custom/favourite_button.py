from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import pyqtSlot

from ..widgets import Button
from ..misc import Icons


class FavouriteBtn(Button):
    def __init__(self, parent: QWidget, is_favourite: bool = False):
        super().__init__(parent, self.__class__.__name__)
        self.is_favourite: bool = is_favourite

    @pyqtSlot()
    def set_favourite(self, slot: callable = lambda: None):
        self.is_favourite = not self.is_favourite
        if self.is_favourite:
            self.setIcon(Icons.STAR_FILL.icon)
        else:
            self.setIcon(Icons.STAR.icon)
        slot()
