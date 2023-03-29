from PyQt5.QtWidgets import QMenuBar


class MenuBar(QMenuBar):
    def __init__(self, parent):
        super().__init__(parent)
        self.setObjectName(self.__class__.__name__)

    async def init(self) -> 'MenuBar':
        settings_menu = self.addMenu('&Settings')
        help_menu = self.addMenu('&Help')
        about_menu = self.addMenu('&About')
        return self
