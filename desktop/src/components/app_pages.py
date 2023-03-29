from PyQt5.QtWidgets import QStackedWidget
from PyQt5.QtCore import Qt

from ..views import SignUp, SignIn
# from ..views.app_view import AppView


class AppPages(QStackedWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.setObjectName(self.__class__.__name__)

    async def init(self) -> 'AppPages':
        self.layout().setAlignment(Qt.AlignHCenter)
        self.addWidget(await SignIn(self).init())
        self.addWidget(await SignUp(self).init())
        # self.addWidget(await AppView(self).init())
        if not self.parent().settings.value('access_token'):
            self.setCurrentIndex(0)
        else:
            self.setCurrentIndex(2)
        return self
