from PyQt5.QtWidgets import QWidget, QFileDialog
from PyQt5.QtCore import pyqtSlot

from ..widgets import Button
from ..utils import Icon


class ImageButton(Button):
    def __init__(self, parent: QWidget, name: str = None, visible: bool = True):
        super().__init__(parent, name if name else self.__class__.__name__, visible)
        self.icon_bytes = None

    def init(
            self, *,
            icon: Icon, slot: callable = lambda: None
    ) -> 'ImageButton':
        super().init(icon=icon, slot=lambda: self.set_icon(slot))
        return self

    @pyqtSlot()
    def set_icon(self, slot: callable = lambda: None):
        dialog = QFileDialog()
        filepath, _ = dialog.getOpenFileName(None, 'Choose image', '', 'Images (*.jpg)', options=dialog.Options())
        if filepath:
            with open(filepath, 'rb') as file:
                icon_bytes = file.read()
                self.icon_bytes = icon_bytes
                self.setIcon(Icon(icon_bytes).icon)
                slot()
