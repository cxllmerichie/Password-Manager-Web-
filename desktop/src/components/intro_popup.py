from aioqui.widgets import Widget, Label, Layout, Spacer, Button, Frame, Popup, Parent
from aioqui.qasyncio import asyncSlot
from aioqui import CONTEXT
from PySide6.QtGui import QResizeEvent

from .. import stylesheets
from ..misc import ICONS, API


class IntroPopup(Widget):
    def __init__(self, parent: Parent):
        super().__init__(parent, self.__class__.__name__, stylesheet=stylesheets.components.fullscreen_popup)

    async def init(self) -> 'IntroPopup':
        self.setLayout(await Layout.vertical().init(
            spacing=10,
            items=[
                await Button(self, 'AuthExitBtn').init(
                    icon=ICONS.CROSS, events=Button.Events(on_click=self.core.close)
                ), Layout.RightTop,
                await Frame(self, 'FullscreenFrame').init(
                    layout=await Layout.vertical().init(
                        alignment=Layout.Center, spacing=10,
                        items=[
                            Spacer(False, True),
                            await Label(self, 'StorageLbl').init(
                                text='How do you want to store your data?', sizes=Label.Sizes(alignment=Layout.Center)
                            ),
                            Spacer(False, True),
                            await Layout.horizontal().init(
                                items=[
                                    LocalBtn := await Button(self, 'StorageBtn').init(
                                        text='[LOCAL] On my computer', events=Button.Events(on_click=self.set_storage_local)
                                    ),
                                    RemoteBtn := await Button(self, 'StorageBtn').init(
                                        text='[REMOTE] On the server', events=Button.Events(on_click=self.set_storage_remote)
                                    )
                                ]
                            ),
                            await Label(self, 'HintLbl1').init(
                                wrap=True, sizes=Label.Sizes(alignment=Layout.Center)
                            ),
                            Spacer(False, True),
                            await Label(self, 'HintLbl2').init(
                                wrap=True, sizes=Label.Sizes(alignment=Layout.Center),
                                text='You will be able to change your choice any time after pressing "Continue" in the '
                                     'bottom panel'
                            ),
                            await Button(self, 'ContinueBtn').init(
                                text='Continue', events=Button.Events(on_click=self.execute_continue)
                            ),
                            Spacer(False, True),
                        ]
                    )
                )
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
        self.LocalBtn.setStyleSheet(stylesheets.components.active_button)
        self.RemoteBtn.setStyleSheet(stylesheets.components.inactive_button)
        self.HintLbl1.setText('Storing data locally gives you access to it any time, also without internet connection. '
                              'Data will be lost in case of storage corruption or uninstalling the application. '
                              'Also a little quicker.')
        CONTEXT['storage'] = API.Storage.LOCAL

    @asyncSlot()
    async def set_storage_remote(self):
        if not await API.is_connected():
            return await Popup(self.core).display(
                buttons=[Popup.OK],
                message='Remote storage is not available at the moment'
            )
        self.LocalBtn.setStyleSheet(stylesheets.components.inactive_button)
        self.RemoteBtn.setStyleSheet(stylesheets.components.active_button)
        self.HintLbl1.setText('Storing data remotely gives you access to it only with internet connection.\n'
                              'Using your personal account in any device gives you access to data. Also a little slower.')
        CONTEXT['storage'] = API.Storage.REMOTE

    def resizeEvent(self, event: QResizeEvent) -> None:
        self.resize(self.parent().size())
