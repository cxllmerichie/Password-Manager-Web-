from qcontext.widgets import Widget, Label, Layout, Spacer, Button, Frame, Popup
from qcontext.qasyncio import asyncSlot
from qcontext import CONTEXT
from PyQt5.QtGui import QResizeEvent
from PyQt5.QtWidgets import QWidget

from .. import stylesheets
from ..misc import utils, ICONS, API


class IntroPopup(Widget):
    def __init__(self, parent: QWidget):
        super().__init__(parent, self.__class__.__name__, stylesheet=stylesheets.components.fullscreen_popup)

    async def init(self) -> 'IntroPopup':
        self.setLayout(await Layout.vertical().init(
            spacing=10,
            items=[
                await Button(self, 'AuthExitBtn').init(
                    icon=ICONS.CROSS, slot=self.core.close
                ), Layout.RightTop,
                await Frame(self, 'FullscreenFrame').init(
                    layout=await Layout.vertical().init(
                        alignment=Layout.Center, spacing=10,
                        items=[
                            Spacer(False, True),
                            await Label(self, 'StorageLbl').init(
                                text='How do you want to store your data?', alignment=Layout.Center
                            ),
                            Spacer(False, True),
                            await Layout.horizontal().init(
                                items=[
                                    LocalBtn := await Button(self, 'StorageBtn').init(
                                        text='[LOCAL] On my computer', slot=self.set_storage_local
                                    ),
                                    RemoteBtn := await Button(self, 'StorageBtn').init(
                                        text='[REMOTE] On the server', slot=self.set_storage_remote
                                    )
                                ]
                            ),
                            await Label(self, 'HintLbl1').init(
                                wrap=True, alignment=Layout.Center
                            ),
                            Spacer(False, True),
                            await Label(self, 'HintLbl2').init(
                                wrap=True, alignment=Layout.Center,
                                text='You will be able to change your choice any time in the left lower corner '
                                     'of the app after pressing "Continue"'
                            ),
                            await Button(self, 'ContinueBtn').init(
                                text='Continue', slot=self.execute_continue
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
        self.HintLbl1.setText('Storing data locally gives you access to the data any time even without '
                              'internet connection but erases in case of file corruption of deleting the storage. '
                              'Also a little quicker.')
        CONTEXT['storage'] = utils.Storage.LOCAL

    @asyncSlot()
    async def set_storage_remote(self):
        if not await API.is_connected():
            return await Popup(self.core).display(
                buttons=[Popup.OK],
                message='Remote storage is not available at the moment'
            )
        self.LocalBtn.setStyleSheet(stylesheets.components.inactive_button)
        self.RemoteBtn.setStyleSheet(stylesheets.components.active_button)
        self.HintLbl1.setText('Storing data remotely gives you access to the data only with internet connection '
                              'and in any device logging in using your personal account. Also a little slower.')
        CONTEXT['storage'] = utils.Storage.REMOTE

    def resizeEvent(self, event: QResizeEvent) -> None:
        self.resize(self.parent().size())
