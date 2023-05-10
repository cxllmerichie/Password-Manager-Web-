from qcontextapi.widgets import Widget, Label, Layout, Spacer, Button, Frame
from PyQt5.QtGui import QResizeEvent
from PyQt5.QtWidgets import QWidget
from qcontextapi import CONTEXT
from qasync import asyncSlot

from .. import stylesheets
from ..misc import utils, ICONS


class FullscreenPopup(Widget):
    def __init__(self, parent: QWidget):
        super().__init__(parent, self.__class__.__name__, stylesheet=stylesheets.components.fullscreen_popup)

    async def init(self) -> 'FullscreenPopup':
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
                                    await Button(self, 'LocalBtn').init(
                                        text='[LOCAL] On my computer', slot=self.storage_choice
                                    ),
                                    await Button(self, 'RemoteBtn').init(
                                        text='[REMOTE] On the server', slot=self.storage_choice
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
        self.LocalBtn.setStyleSheet(stylesheets.components.inactive_button)
        self.RemoteBtn.setStyleSheet(stylesheets.components.active_button)
        self.HintLbl1.setText('Storing data remotely gives you access to the data only with internet connection '
                              'and in any device logging in using your personal account. Also a little slower.')
        return self

    @asyncSlot()
    async def execute_continue(self):
        if self.LocalBtn.styleSheet() == stylesheets.components.active_button:
            CONTEXT['storage'] = utils.Storage.LOCAL
        else:
            CONTEXT['storage'] = utils.Storage.REMOTE
        await self.core.init()
        self.deleteLater()

    @asyncSlot()
    async def storage_choice(self):
        name = self.sender().objectName()
        if name == 'LocalBtn':
            self.LocalBtn.setStyleSheet(stylesheets.components.active_button)
            self.RemoteBtn.setStyleSheet(stylesheets.components.inactive_button)
            self.HintLbl1.setText('Storing data locally gives you access to the data any time even without '
                                  'internet connection but erases in case of file corruption of deleting the storage. '
                                  'Also a little quicker.')
        else:
            self.LocalBtn.setStyleSheet(stylesheets.components.inactive_button)
            self.RemoteBtn.setStyleSheet(stylesheets.components.active_button)
            self.HintLbl1.setText('Storing data remotely gives you access to the data only with internet connection '
                                  'and in any device logging in using your personal account. Also a little slower.')

    def resizeEvent(self, event: QResizeEvent) -> None:
        self.resize(self.parent().size())
