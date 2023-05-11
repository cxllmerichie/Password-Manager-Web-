from qcontextapi.widgets import Button, Label, LineInput, Layout, Spacer, Frame, Widget
from qcontextapi.customs import ErrorLabel
from qcontextapi import CONTEXT
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt, pyqtSlot
import email_validator
from qasync import asyncSlot

from ..misc import ICONS, API
from .. import stylesheets


class SignUp(Widget):
    def __init__(self, parent: QWidget):
        super().__init__(parent, self.__class__.__name__, stylesheet=stylesheets.view_signup.css)

    async def init(self) -> 'SignUp':
        self.setLayout(await Layout.vertical().init(
            spacing=10, alignment=Qt.AlignVCenter,
            items=[
                await Button(self, 'AuthExitBtn').init(
                    icon=ICONS.CROSS, slot=self.core.close
                ), Layout.RightTop,
                Spacer(False, True),
                await Label(self, 'InfoLbl').init(
                    text='Registration'
                ), Layout.HCenter,
                Spacer(False, True),
                await Frame(self, 'InputFrameEmail').init(
                    layout=await Layout.vertical(self).init(
                        margins=(5, 5, 5, 5), spacing=5, alignment=Layout.Center,
                        items=[
                            await Label(self, 'InputLabelEmail').init(
                                text='Email'
                            ),
                            await LineInput(self, 'InputFieldEmail').init(
                                placeholder='address@domain.tld', textchanged=self.validate_email
                            )
                        ]
                    )
                ), Qt.AlignHCenter,
                await Frame(self, 'InputFramePassword').init(
                    layout=await Layout.vertical(self).init(
                        margins=(5, 5, 5, 5), spacing=5, alignment=Layout.Center,
                        items=[
                            await Label(self, 'InputLabelPassword').init(
                                text='Password'
                            ),
                            await LineInput(self, 'InputFieldPassword').init(
                                placeholder='password', hidden=True, textchanged=self.validate_password
                            )
                        ]
                    )
                ), Qt.AlignHCenter,
                await Frame(self, 'InputFrameConfpass').init(
                    layout=await Layout.vertical(self).init(
                        margins=(5, 5, 5, 5), spacing=5, alignment=Layout.Center,
                        items=[
                            await Label(self, 'InputLabelConfpass').init(
                                text='Confirm password'
                            ),
                            await LineInput(self, 'InputFieldConfpass').init(
                                placeholder='password', hidden=True, textchanged=self.validate_confpass
                            )
                        ]
                    )
                ), Qt.AlignHCenter,
                await ErrorLabel(self, 'ErrorLbl').init(
                    wrap=True, alignment=Layout.Center
                ), Layout.Center,
                await Button(self, 'AuthTextBtn').init(
                    text='Already have an account?', slot=lambda: CONTEXT.CentralWidget.setCurrentIndex(0)
                ), Qt.AlignHCenter,
                await Button(self, 'AuthMainBtn').init(
                    text='Create Account', slot=self.sign_up
                ), Qt.AlignHCenter,
                Spacer(False, True)
            ]
        ))
        return self

    @asyncSlot()
    async def validate_email(self):
        error = ''
        try:
            email_validator.validate_email(self.InputFieldEmail.text())
        except Exception as exception:
            error = str(exception)
        self.ErrorLbl.setText(error)
        return len(error) == 0

    @asyncSlot()
    async def validate_password(self):
        error = ''
        if len(self.InputFieldPassword.text()) < 8:
            error = 'Password length must be greater than 8'
        self.ErrorLbl.setText(error)
        return len(error) == 0

    @asyncSlot()
    async def validate_confpass(self):
        error = ''
        if self.InputFieldPassword.text() != self.InputFieldConfpass.text():
            error = 'Password and confirmation password do not match'
        self.ErrorLbl.setText(error)
        return len(error) == 0

    @asyncSlot()
    async def sign_up(self):
        if not self.validate_email():
            return
        if not self.validate_password():
            return
        if not self.validate_confpass():
            return
        created_user = await API.create_user({
            'email': self.InputFieldEmail.text(), 'password': self.InputFieldPassword.text()
        })
        if not (token := created_user.get('access_token')):
            return self.ErrorLbl.setText('Internal error, please try again')
        await CONTEXT.LeftMenu.refresh_categories(await API.get_categories())
        CONTEXT.CentralWidget.setCurrentWidget(CONTEXT.MainView)
