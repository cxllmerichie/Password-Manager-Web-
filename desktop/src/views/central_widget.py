from aioqui.widgets import StackedWidget, Parent
from aioqui.asynq import asyncSlot
from aioqui import CONTEXT

from .view_signin import SignIn
from .view_signup import SignUp
from .view_main import MainView
from ..misc import Storage


class CentralWidget(StackedWidget):
    def __init__(self, parent: Parent):
        super().__init__(parent, self.__class__.__name__)

    async def init(self) -> 'CentralWidget':
        await super().init(
            on_change=self.current_widget_changed,
            items=[
                await SignIn(self).init(),
                await SignUp(self).init(),
                await MainView(self).init()
            ]
        )
        if CONTEXT['storage'] == Storage.LOCAL or CONTEXT['token']:
            self.setCurrentWidget(CONTEXT.MainView)
        else:
            self.setCurrentWidget(CONTEXT.SignIn)
        return self

    @asyncSlot()
    async def current_widget_changed(self):
        CONTEXT.LogoutBtn.setVisible(CONTEXT['token'] is not None)
        is_main = self.currentWidget().objectName() == 'MainView'
        CONTEXT.Panel.ToggleMenuBtn.setVisible(is_main)
        if is_main:
            await CONTEXT.LeftMenu.refresh_categories()
            await CONTEXT.CentralItems.refresh_items([])
            await CONTEXT.RightPagesCategory.show_create()
            CONTEXT.RightPages.shrink()
