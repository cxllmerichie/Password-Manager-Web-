from aioqui.widgets import Layout, Label, Selector, Frame, Button, StatusBar as StatusBarBase
from aioqui.widgets.custom import Popup
from aioqui.asynq import asyncSlot
from aioqui import CONTEXT

from ..misc import API, ICONS, Storage
from .. import qss


class StatusBar(StatusBarBase):
    def __init__(self, parent):
        super().__init__(parent, self.__class__.__name__)
        # styleSheet is set in the `app.py`, where the `StatusBar` is imported, otherwise does not work

    async def init(self) -> 'StatusBar':
        self.addWidget(await Frame(self, 'LeftFrame', qss='border: none').init(
            layout=await Layout.horizontal().init(
                alignment=Layout.Left,
                items=[
                    await Button(self, 'LogoutBtn').init(
                        icon=ICONS.LOGOUT, text='Log out', on_click=Popup(
                            self.core, qss=qss.components.popup,
                            message=f'Do you want to log out?',
                            on_success=self.log_out
                        ).display
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
                        items=[
                            Selector.Item(text=Storage.LOCAL),
                            Selector.Item(text=Storage.REMOTE),
                        ]
                    ), Layout.Left,
                ]
            )
        ), 3)
        self.addWidget(await Frame(self, 'RightFrame').init(

        ), 3)
        # order matters, since `currentText` is initial, and we do not want to trigger `textChanged`
        self.StorageSelector.setCurrentText(CONTEXT['storage'])
        self.StorageSelector = await self.StorageSelector.init(on_change=self.storage_selector_textchanged)
        return self

    def log_out(self):
        CONTEXT['token'] = None
        self.StorageSelector.setCurrentText(Storage.REMOTE)

    @asyncSlot()
    async def storage_selector_textchanged(self):
        # if trying to switch to remote, but api is not active at the moment
        if self.StorageSelector.currentText() == Storage.REMOTE and not await API.is_connected():
            await Popup(self.core).display(
                message='Remote storage is not available at the moment', buttons=[Popup.OK],
            )
            return self.StorageSelector.setCurrentText(Storage.LOCAL)
        CONTEXT['storage'] = self.StorageSelector.currentText()
        if CONTEXT['storage'] == Storage.REMOTE and not CONTEXT['token']:
            return CONTEXT.CentralWidget.setCurrentWidget(CONTEXT.SignIn)
        if CONTEXT.CentralWidget.currentWidget().objectName() == 'MainView':
            await CONTEXT.LeftMenu.refresh_categories()
            await CONTEXT.CentralItems.refresh_items([])
            await CONTEXT.RightPagesCategory.show_create()
            CONTEXT.RightPages.shrink()
        CONTEXT.CentralWidget.setCurrentWidget(CONTEXT.MainView)
