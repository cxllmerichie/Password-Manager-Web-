from qcontext.widgets import StackedWidget
from qcontext.qasyncio import asyncSlot
from qcontext import CONTEXT
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt

from .view_signin import SignIn
from .view_signup import SignUp
from .view_main import MainView
from ..misc import utils


class CentralWidget(StackedWidget):
    def __init__(self, parent: QWidget):
        super().__init__(parent, self.__class__.__name__)
        self.currentChanged.connect(self.current_widget_changed)

    async def init(self) -> 'CentralWidget':
        self.layout().setAlignment(Qt.AlignHCenter)
        self.addWidget(await SignIn(self).init())
        self.addWidget(await SignUp(self).init())
        self.addWidget(await MainView(self).init())
        if CONTEXT['storage'] == utils.Storage.LOCAL or CONTEXT['token']:
            self.setCurrentWidget(CONTEXT.MainView)
        else:
            self.setCurrentWidget(CONTEXT.SignIn)
        return self

    @asyncSlot()
    async def current_widget_changed(self):
        CONTEXT.LogoutBtn.setVisible(CONTEXT['token'] is not None)
        if self.currentWidget().objectName() == 'MainView':
            await CONTEXT.LeftMenu.refresh_categories()
            await CONTEXT.RightPagesCategory.show_create()
            CONTEXT.RightPages.shrink()
