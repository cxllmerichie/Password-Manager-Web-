from aioqui.widgets import Label, Layout, Spacer, Button, Frame, Parent
from aioqui.widgets.custom import Popup
from aioqui.asynq import asyncSlot
from aioqui import CONTEXT
from PySide6.QtGui import QResizeEvent

from .. import qss
from ..misc import ICONS, API, Storage


class IntroPopup(Frame):
    def __init__(self, parent: Parent):
        super().__init__(parent, self.__class__.__name__, qss=qss.components.intro_popup)

    async def init(self) -> 'IntroPopup':
        self.setLayout(await Layout.vertical().init(
            alignment=Layout.Center, spacing=10,
            items=[
                Spacer(hpolicy=Spacer.Expanding),
                await Label(self, 'StorageLbl').init(
                    text='How do you want to store your data?', alignment=Layout.Center
                ),
                Spacer(hpolicy=Spacer.Expanding),
                await Layout.horizontal().init(
                    items=[
                        LocalBtn := await Button(self, 'StorageBtn').init(
                            text='[LOCAL] On my computer', on_click=self.set_storage_local
                        ),
                        RemoteBtn := await Button(self, 'StorageBtn').init(
                            text='[REMOTE] On the server', on_click=self.set_storage_remote
                        )
                    ]
                ),
                await Label(self, 'HintLbl1').init(
                    wrap=True, alignment=Layout.Center
                ),
                Spacer(hpolicy=Spacer.Expanding),
                await Label(self, 'HintLbl2').init(
                    wrap=True, alignment=Layout.Center,
                    text='You will be able to change your choice any time after pressing "Continue" in the '
                         'bottom panel'
                ),
                await Button(self, 'ContinueBtn').init(
                    text='Continue', on_click=self.execute_continue
                ),
                Spacer(hpolicy=Spacer.Expanding),
            ]
        ))
        self.LocalBtn = LocalBtn
        self.RemoteBtn = RemoteBtn
        await self.set_storage_local()
        return self

    @asyncSlot()
    async def execute_continue(self):
        await self.core.init()
        self.deleteLater()

    @asyncSlot()
    async def set_storage_local(self):
        self.LocalBtn.setStyleSheet(qss.components.active_button)
        self.RemoteBtn.setStyleSheet(qss.components.inactive_button)
        self.HintLbl1.setText('Storing data locally gives you access to it any time, also without internet connection. '
                              'Data will be lost in case of storage corruption or uninstalling the application. '
                              'Also a little quicker.')
        CONTEXT['storage'] = Storage.LOCAL

    @asyncSlot()
    async def set_storage_remote(self):
        if not await API.is_connected():
            return await Popup(self.core).display(
                buttons=[Popup.OK],
                message='Remote storage is not available at the moment'
            )
        self.LocalBtn.setStyleSheet(qss.components.inactive_button)
        self.RemoteBtn.setStyleSheet(qss.components.active_button)
        self.HintLbl1.setText('Storing data remotely gives you access to it only with internet connection.\n'
                              'Using your personal account in any device gives you access to data. Also a little slower.')
        CONTEXT['storage'] = Storage.REMOTE

    def resizeEvent(self, event: QResizeEvent) -> None:
        self.resize(self.parent().size())
