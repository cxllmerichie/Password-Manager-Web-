from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt

from ._wrapper import Wrapper


class SideMenu(Wrapper):
    def __init__(self, parent: QWidget, name: str, visible: bool = True,
                 expand_to: int = None, expand_orientation: Qt.Orientation = Qt.Horizontal):
        Wrapper.__init__(self, parent, name, visible)
        if not expand_to:
            raise AttributeError(f'`size` is not specified in `SideMenu` constructor')
        self.expand_to = expand_to
        self.expand_orientation = expand_orientation

    def __dimension(self):
        return self.width() if self.expand_orientation is Qt.Horizontal else self.height()

    def expand(self, expand_to: int = None):
        if expand_to:
            self.expand_to = expand_to
        self.setFixedWidth(self.expand_to)

    def shrink(self) -> None:
        self.setFixedWidth(0)

    def toggle(self) -> None:
        self.expand() if self.__dimension() == 0 else self.shrink()
