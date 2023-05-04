from qcontextapi.widgets import Label, Layout, Frame
from qcontextapi.misc import Icon
from PyQt5.QtWidgets import QWidget


class ProfileButton(Frame):
    def __init__(self, parent: QWidget):
        super().__init__(parent, self.__class__.__name__)

    def init(self, icon: Icon.IconType, text: str, slot: callable = None) -> 'ProfileButton':
        self.setLayout(Layout.horizontal().init(
            margins=(10, 0, 10, 0), spacing=10, alignment=Layout.Center,
            items=[
                Label(self, 'ProfileButtonIcon').init(
                    icon=icon
                ),
                Label(self, 'ProfileButtonText').init(
                    text=text
                )
            ]
        ))
        self.mousePressEvent = lambda event: slot()
        return self
