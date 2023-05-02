from PyQt5.QtWidgets import QWidget, QFileDialog
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QIcon

from ..widgets import Button
from ..misc import Icon


class ImageButton(Button):
    def __init__(self, parent: QWidget, name: str = None, visible: bool = True):
        super().__init__(parent, name if name else self.__class__.__name__, visible)
        self.image_bytes = None

    @property
    def image_bytes_str(self) -> str | None:
        return str(self.image_bytes) if self.image_bytes else None

    def init(
            self, *,
            icon: Icon, slot: callable = lambda: None
    ) -> 'ImageButton':
        super().init(icon=icon, slot=lambda: self.choose_image(slot))
        return self

    def setIcon(self, icon: QIcon) -> None:
        self.image_bytes = Icon.bytes(icon, self.iconSize())
        super().setIcon(icon)

    @pyqtSlot()
    def choose_image(self, slot: callable = lambda: None):
        dialog = QFileDialog()
        filepath, _ = dialog.getOpenFileName(self, 'Choose image', '', 'Images (*.jpg)', options=dialog.Options())
        if filepath:
            with open(filepath, 'rb') as file:
                self.setIcon(Icon(file.read()).icon)
            slot()
