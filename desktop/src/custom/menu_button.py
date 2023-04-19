from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt

from ..widgets import Label, Layout, Button
from ..misc import Icon


class MenuButton(Button):
    def __init__(self, parent: QWidget):
        super().__init__(parent, self.__class__.__name__)

    def init(
            self, *,
            icon: Icon, text: str, total: int,
            alignment: Qt.Alignment = None, slot: callable = lambda: None
    ) -> 'MenuButton':
        self.setLayout(Layout.horizontal().init(
            margins=(10, 0, 0, 0), spacing=10, alignment=Qt.AlignLeft,
            items=[
                Button(self, 'MenuButtonIconBtn').init(
                    size=icon.size, icon=icon, disabled=True
                ),
                Label(self, 'MenuButtonTextLbl').init(
                    text=text, alignment=alignment, elided=True
                ),
                Label(self, 'MenuButtonTotalLbl').init(
                    text=str(total)
                ), Qt.AlignRight
            ]
        ))
        self.clicked.connect(slot)
        return self
