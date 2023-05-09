from qcontextapi.widgets import Layout, Label, Selector, Frame, Button, Popup, StatusBar as CStatusBar
from PyQt5.QtCore import pyqtSlot
from qcontextapi import CONTEXT

from ..misc import utils, API, ICONS
from .. import stylesheets


class StatusBar(CStatusBar):
    def __init__(self, parent):
        super().__init__(parent, self.__class__.__name__)
        # styleSheet is set in the `app.py`, where the `StatusBar` is imported, otherwise does not work

    def init(self) -> 'StatusBar':
        self.addWidget(Frame(self, 'LeftFrame', stylesheet='border: none').init(
            layout=Layout.horizontal().init(
                alignment=Layout.Left,
                items=[
                    Button(self, 'LogoutBtn').init(
                        icon=ICONS.LOGOUT, text='Log out',
                        slot=lambda: Popup(self.core, stylesheet=stylesheets.components.popup).init(
                            message=f'Do you want to log out?',
                            on_success=self.log_out
                        )
                    )
                ]
            )
        ), 3)
        self.addWidget(Frame(self, 'CenterFrame').init(
            layout=Layout.horizontal().init(
                alignment=Layout.VCenter,
                items=[
                    Label(self, 'StorageLbl').init(
                        text='Storage type:'
                    ), Layout.Right,
                    Selector(self, 'StorageSelector').init(
                        textchanged=self.storage_selector_textchanged,
                        items=[
                            Selector.Item(text=utils.Storage.LOCAL.value),
                            Selector.Item(text=utils.Storage.REMOTE.value),
                        ]
                    ), Layout.Left,
                ]
            )
        ), 3)
        self.addWidget(Frame(self, 'RightFrame'), 3)
        return self

    def log_out(self):
        CONTEXT['token'] = None
        CONTEXT.CentralWidget.setCurrentWidget(CONTEXT.SignIn)

    def post_init(self):
        self.StorageSelector.setCurrentText(CONTEXT['storage'].value)

    @pyqtSlot()
    def storage_selector_textchanged(self):
        if self.StorageSelector.currentText() == utils.Storage.LOCAL.value:
            CONTEXT['storage'] = utils.Storage.LOCAL
        else:
            CONTEXT['storage'] = utils.Storage.REMOTE
            if not CONTEXT['token']:
                return CONTEXT.CentralWidget.setCurrentWidget(CONTEXT.SignIn)
        CONTEXT.CentralWidget.setCurrentWidget(CONTEXT.MainView)
        CONTEXT.LeftMenu.refresh_categories(API.get_categories())
        CONTEXT.RightPagesCategory.show_create()
        CONTEXT.RightPages.shrink()
