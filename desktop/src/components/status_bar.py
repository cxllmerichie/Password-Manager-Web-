from PyQt5.QtWidgets import QStatusBar


class StatusBar(QStatusBar):
    def __init__(self, parent):
        super().__init__(parent)
        self.setObjectName(self.__class__.__name__)

    async def init(self) -> 'StatusBar':
        self.showMessage('Password Manager')
        self.setStyleSheet('color: black;')
        return self
