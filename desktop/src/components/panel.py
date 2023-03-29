from PyQt5.QtWidgets import QWidget


class Panel(QWidget):
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self.setObjectName(self.__class__.__name__)

    async def init(self) -> 'Panel':
        return self
