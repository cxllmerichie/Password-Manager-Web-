from qcontext.widgets import Layout, Label, Selector, Frame, Button, Popup, StatusBar as CStatusBar
from qcontext.qasyncio import asyncSlot
from qcontext import CONTEXT

from ..misc import API, ICONS
from .. import stylesheets


class StatusBar(CStatusBar):
    def __init__(self, parent):
        super().__init__(parent, self.__class__.__name__)
        # styleSheet is set in the `app.py`, where the `StatusBar` is imported, otherwise does not work

    async def init(self) -> 'StatusBar':
        self.addWidget(await Frame(self, 'LeftFrame', stylesheet='border: none').init(
            layout=await Layout.horizontal().init(
                alignment=Layout.Left,
                items=[
                    await Button(self, 'LogoutBtn').init(
                        icon=ICONS.LOGOUT, text='Log out',
                        slot=lambda: Popup(self.core, stylesheet=stylesheets.components.popup).display(
                            message=f'Do you want to log out?',
                            on_success=self.log_out
                        )
                    )
                ]
            )
        ), 3)
        self.addWidget(await Frame(self, 'CenterFrame').init(
            layout=await Layout.horizontal().init(
                alignment=Layout.VCenter,
                items=[
                    await Label(self, 'StorageLbl').init(
                        text='Storage type:'
                    ), Layout.Right,
                    await Selector(self, 'StorageSelector').init(
                        textchanged=self.storage_selector_textchanged,
                        items=[
                            Selector.Item(text=API.Storage.LOCAL),
                            Selector.Item(text=API.Storage.REMOTE),
                        ]
                    ), Layout.Left,
                ]
            )
        ), 3)
        self.addWidget(await Frame(self, 'RightFrame').init(

        ), 3)
        return self

    def log_out(self):
        CONTEXT['token'] = None
        self.StorageSelector.setCurrentText(API.Storage.REMOTE)

    async def post_init(self):
        self.StorageSelector.setCurrentText(CONTEXT['storage'])

    @asyncSlot()
    async def storage_selector_textchanged(self):
        if self.StorageSelector.currentText() == API.Storage.REMOTE and not await API.is_connected():
            await Popup(self.core).display(
                buttons=[Popup.OK],
                message='Remote storage is not available at the moment'
            )
            return self.StorageSelector.setCurrentText(API.Storage.LOCAL)
        CONTEXT['storage'] = self.StorageSelector.currentText()
        if CONTEXT['storage'] == API.Storage.REMOTE and not CONTEXT['token']:
            return CONTEXT.CentralWidget.setCurrentWidget(CONTEXT.SignIn)
        await CONTEXT.LeftMenu.refresh_categories(await API.get_categories())
        CONTEXT.CentralWidget.setCurrentWidget(CONTEXT.MainView)
