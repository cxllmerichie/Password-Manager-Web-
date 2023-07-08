from PySide6.QtCore import Qt
from PySide6.QtGui import QKeyEvent
from aioqui.widgets import Button, Label, Input, Layout, Spacer, Frame, Parent
from aioqui.widgets.custom import DurationLabel
from aioqui.asynq import asyncSlot
from aioqui import CONTEXT
import email_validator

from ..misc import api
from .. import qss


class SignUp(Frame):
    def __init__(self, parent: Parent):
        super().__init__(parent, self.__class__.__name__, qss=qss.view_signup.css)

    async def init(self) -> 'SignUp':
        self.setLayout(await Layout.vertical().init(
            spacing=10, alignment=Layout.VCenter,
            items=[
                Spacer(hpolicy=Spacer.Expanding),
                await Label(self, 'InfoLbl').init(
                    text='Registration'
                ), Layout.HCenter,
                Spacer(hpolicy=Spacer.Expanding),
                await Frame(self, 'EmailFrm').init(
                    layout=await Layout.vertical(self).init(
                        margins=(5, 5, 5, 5), spacing=5, alignment=Layout.Center,
                        items=[
                            await Label(self, 'EmailLbl').init(
                                text='Email'
                            ),
                            await Input.line(self, 'EmailInp').init(
                                placeholder='address@domain.tld', on_change=self.validate_email
                            )
                        ]
                    )
                ), Layout.HCenter,
                await Frame(self, 'PasswordFrm').init(
                    layout=await Layout.vertical(self).init(
                        margins=(5, 5, 5, 5), spacing=5, alignment=Layout.Center,
                        items=[
                            await Label(self, 'PasswordLbl').init(
                                text='Password'
                            ),
                            await Input.line(self, 'PasswordInp').init(
                                placeholder='password', hidden=True, on_change=self.validate_password
                            )
                        ]
                    )
                ), Layout.HCenter,
                await Frame(self, 'ConfpassFrm').init(
                    layout=await Layout.vertical(self).init(
                        margins=(5, 5, 5, 5), spacing=5, alignment=Layout.Center,
                        items=[
                            await Label(self, 'ConfpassLbl').init(
                                text='Confirm password'
                            ),
                            await Input.line(self, 'ConfpassInp').init(
                                placeholder='password', hidden=True, on_change=self.validate_confpass
                            )
                        ]
                    )
                ), Layout.HCenter,
                await DurationLabel(self, 'ErrorLbl').init(
                    wrap=True, alignment=Layout.Center
                ), Layout.Center,
                await Button(self, 'TextBtn').init(
                    text='Already have an account?', on_click=lambda: CONTEXT.CentralWidget.setCurrentIndex(0)
                ), Layout.HCenter,
                await Button(self, 'MainBtn').init(
                    text='Create Account', on_click=self.sign_up
                ), Layout.HCenter,
                Spacer(hpolicy=Spacer.Expanding)
            ]
        ))
        return self

    def keyPressEvent(self, event: QKeyEvent) -> None:
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.MainBtn.click()
        super().keyPressEvent(event)

    @asyncSlot()
    async def validate_email(self):
        error = ''
        try:
            email_validator.validate_email(self.EmailInp.text())
        except Exception as exception:
            error = str(exception)
        self.ErrorLbl.setText(error)
        return len(error) == 0

    @asyncSlot()
    async def validate_password(self):
        error = ''
        if len(self.PasswordInp.text()) < 8:
            error = 'Password length must be greater than 8'
        self.ErrorLbl.setText(error)
        return len(error) == 0

    @asyncSlot()
    async def validate_confpass(self):
        error = ''
        if self.PasswordInp.text() != self.ConfpassInp.text():
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
        created_user = await api.create_user({
            'email': self.EmailInp.text(), 'password': self.PasswordInp.text()
        })
        if not (token := created_user.get('access_token')):
            return self.ErrorLbl.setText('Internal error, please try again')
        self.EmailInp.setText('')
        self.PasswordInp.setText('')
        self.ConfpassInp.setText('')
        CONTEXT.CentralWidget.setCurrentWidget(CONTEXT.MainView)
