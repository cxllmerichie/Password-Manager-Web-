from PyQt5.QtWidgets import QWidget, QStackedWidget


class ExpandWidget(QStackedWidget):
    def __init__(self, parent: QWidget, width: int):
        super().__init__(parent)
        self._width = width

    async def init(self):
        return self

    async def expand(self):
        self.setFixedWidth(self._width)

    async def shrink(self):
        self.setFixedWidth(0)
