from PyQt5.QtWidgets import QWidget

from ..widgets import VBox, HBox
from ..components import LeftPages, RightPages, CenterPages, Panel


class AppView(QWidget):
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self.setObjectName(self.__class__.__name__)

    async def __layout(self) -> VBox:
        vbox = await VBox().init()

        hbox = await HBox(self).init()
        hbox.addWidget(await LeftPages(self, 200).init())
        hbox.addWidget(await CenterPages(self).init())
        hbox.addWidget(await RightPages(self, 200).init())

        vbox.addWidget(await Panel(self).init())
        vbox.addLayout(hbox)
        return vbox

    async def init(self) -> 'AppView':
        return self
