from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import pyqtSlot

from ..widgets import Button
from ..misc import Icons, Icon


class FavouriteButton(Button):
    def __init__(self, parent: QWidget, is_favourite: bool = False):
        super().__init__(parent, self.__class__.__name__)
        self.is_favourite: bool = is_favourite

    def init(
            self, *,
            icon: Icon = None, slot: callable = lambda: None
    ) -> 'Button':
        super().init(icon=icon, slot=lambda: self.slot(slot))
        return self

    @pyqtSlot()
    def slot(self, slot: callable = lambda: None):
        self.set(not self.is_favourite)
        slot()

    def set_favourite(self):
        self.setIcon(Icons.STAR_FILL.icon)
        self.is_favourite = True

    def unset_favourite(self):
        self.setIcon(Icons.STAR.icon)
        self.is_favourite = False

    def set(self, is_favourite: bool):
        self.is_favourite = is_favourite
        if self.is_favourite:
            self.set_favourite()
        else:
            self.unset_favourite()
