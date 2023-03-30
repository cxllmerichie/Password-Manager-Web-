from PyQt5.QtWidgets import QStackedWidget, QWidget
from PyQt5.QtCore import Qt

from desktop.src.views import SignUp, SignIn
from ..widgets import VBox, HBox
from ..components import LeftMenu, RightPages, CenterPages, Panel


class AppPages(QStackedWidget):
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self.setObjectName(self.__class__.__name__)

    async def init(self) -> 'AppPages':
        self.layout().setAlignment(Qt.AlignHCenter)
        self.addWidget(await SignIn(self).init())
        self.addWidget(await SignUp(self).init())
        self.addWidget(await AppView(self).init())
        if not self.parent().settings.value('access_token'):
            self.setCurrentIndex(0)
        else:
            self.setCurrentIndex(2)
        return self


class AppView(QWidget):
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self.setObjectName(self.__class__.__name__)

    async def __layout(self) -> VBox:
        vbox = await VBox().init()

        hbox = await HBox(self).init()
        hbox.addWidget(await LeftMenu(self, 200).init())
        hbox.addWidget(await CenterPages(self).init())
        hbox.addWidget(await RightPages(self, 200).init())

        vbox.addWidget(await Panel(self).init())
        vbox.addLayout(hbox)
        return vbox

    async def init(self) -> 'AppView':
        self.setLayout(await self.__layout())
        return self
