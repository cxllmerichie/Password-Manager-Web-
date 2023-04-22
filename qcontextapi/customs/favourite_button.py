from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import pyqtSlot
from typing import Callable

from ..widgets import Button
from ..utils import Icon


class FavouriteButton(Button):
    def __init__(self, parent: QWidget, is_favourite: bool = False):
        super().__init__(parent, self.__class__.__name__)
        self.__is_favourite: bool = is_favourite
        self.if_set_icon: Icon = Icon('star-fill.svg', (30, 30))
        self.if_unset_icon: Icon = Icon('star.svg', (30, 30))

    def init(
            self, *,
            if_set_icon: Icon = None, if_unset_icon: Icon = None, pre_slot: Callable[[...], bool] = lambda: None
    ) -> 'Button':
        super().init(icon=if_unset_icon, slot=lambda: self.slot(pre_slot))
        if if_set_icon:
            self.if_set_icon = if_set_icon
        if if_unset_icon:
            self.if_unset_icon = if_unset_icon
        return self

    @pyqtSlot()
    def slot(self, pre_slot: callable = lambda: None):
        # toggle to change state
        self.set(not self.is_favourite)
        if not pre_slot():
            # toggle once more to come back to prev state if `pre_slot` returns `False`
            self.set(not self.is_favourite)

    def set_favourite(self):
        self.setIcon(self.if_set_icon.icon)
        self.setIconSize(self.if_set_icon.size)
        self.is_favourite = True

    def unset_favourite(self):
        self.setIcon(self.if_unset_icon.icon)
        self.setIconSize(self.if_unset_icon.size)
        self.is_favourite = False

    def set(self, is_favourite: bool):
        self.is_favourite = is_favourite
        if self.is_favourite:
            self.set_favourite()
        else:
            self.unset_favourite()
