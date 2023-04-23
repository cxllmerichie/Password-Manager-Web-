from PyQt5.QtWidgets import QWidget, QSizePolicy
from PyQt5.QtCore import Qt

from ..widgets import Label, Layout, Button
from ..utils import Icon


class MenuButton(Button):
    def __init__(self, parent: QWidget):
        super().__init__(parent, self.__class__.__name__)

    def init(
            self, *,
            icon: Icon, text: str, total: int = 0, alignment: Qt.Alignment = None, slot: callable = lambda: None
    ) -> 'MenuButton':
        self.setLayout(Layout.horizontal().init(
            margins=(10, 5, 10, 5), spacing=10,
            items=[
                Button(self, f'{self.objectName()}IconBtn').init(
                    size=icon.size, icon=icon, disabled=True
                ), Layout.Left,
                Label(self, f'{self.objectName()}TextLbl').init(
                    text=text, alignment=alignment, elided=True, policy=(QSizePolicy.Expanding, QSizePolicy.Minimum)
                ),
                Label(self, f'{self.objectName()}TotalLbl').init(
                    text=str(total)
                ), Layout.Right
            ]
        ))
        self.clicked.connect(slot)
        return self
