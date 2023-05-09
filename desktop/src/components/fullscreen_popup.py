from PyQt5.QtGui import QResizeEvent
from qcontextapi.widgets import Widget, Label, Layout, Spacer, Button, Frame
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import pyqtSlot
from qcontextapi import CONTEXT

from .. import css
from ..misc import utils, ICONS


class FullscreenPopup(Widget):
    def __init__(self, parent: QWidget):
        super().__init__(parent, self.__class__.__name__, stylesheet=css.components.fullscreen_popup)

    def init(self) -> 'FullscreenPopup':
        self.setLayout(Layout.vertical().init(
            spacing=10,
            items=[
                Button(self, 'AuthExitBtn').init(
                    icon=ICONS.CROSS, slot=self.core.close
                ), Layout.RightTop,
                Frame(self, 'FullscreenFrame').init(
                    layout=Layout.vertical().init(
                        alignment=Layout.Center, spacing=10,
                        items=[
                            Spacer(False, True),
                            Label(self, 'StorageLbl').init(
                                text='How do you want to store your data?', alignment=Layout.Center
                            ),
                            Spacer(False, True),
                            Layout.horizontal().init(
                                items=[
                                    Button(self, 'LocalBtn').init(
                                        text='[LOCAL] On my computer', slot=self.storage_choice
                                    ),
                                    Button(self, 'RemoteBtn').init(
                                        text='[REMOTE] On the server', slot=self.storage_choice
                                    )
                                ]
                            ),
                            Label(self, 'HintLbl1').init(
                                wrap=True, alignment=Layout.Center
                            ),
                            Spacer(False, True),
                            Label(self, 'HintLbl2').init(
                                wrap=True, alignment=Layout.Center,
                                text='You will be able to change your choice any time in the left lower corner '
                                     'of the app after pressing "Continue"'
                            ),
                            Button(self, 'ContinueBtn').init(
                                text='Continue', slot=self.execute_continue
                            ),
                            Spacer(False, True),
                        ]
                    )
                )
            ]
        ))
        self.RemoteBtn.click()
        return self

    @pyqtSlot()
    def execute_continue(self):
        if self.LocalBtn.styleSheet() == css.components.active_button:
            CONTEXT['storage'] = utils.Storage.LOCAL
        else:
            CONTEXT['storage'] = utils.Storage.REMOTE
        self.setVisible(False)
        self.hide()
        self.core.init()

    @pyqtSlot()
    def storage_choice(self):
        name = self.sender().objectName()
        if name == 'LocalBtn':
            self.LocalBtn.setStyleSheet(css.components.active_button)
            self.RemoteBtn.setStyleSheet(css.components.inactive_button)
            self.HintLbl1.setText('Storing data locally gives you access to the data any time even without '
                                  'internet connection but erases in case of file corruption of deleting the storage. '
                                  'Also a little quicker.')
        else:
            self.LocalBtn.setStyleSheet(css.components.inactive_button)
            self.RemoteBtn.setStyleSheet(css.components.active_button)
            self.HintLbl1.setText('Storing data remotely gives you access to the data only with internet connection '
                                  'and in any device logging in using your personal account. Also a little slower.')

    def resizeEvent(self, event: QResizeEvent) -> None:
        self.resize(self.parent().size())
