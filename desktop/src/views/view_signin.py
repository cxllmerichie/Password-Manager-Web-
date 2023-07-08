from PySide6.QtCore import Qt
from PySide6.QtGui import QKeyEvent
from aioqui.widgets import Button, Label, Input, Frame, Layout, Spacer, Parent
from aioqui.widgets.custom import DurationLabel
from aioqui.asynq import asyncSlot
from aioqui import CONTEXT

from ..misc import api
from .. import qss


class SignIn(Frame):
    def __init__(self, parent: Parent):
        super().__init__(parent, self.__class__.__name__, qss=qss.view_signin.css)

    async def init(self) -> 'SignIn':
        self.setLayout(await Layout.vertical().init(
            spacing=10, alignment=Layout.VCenter,
            items=[
                Spacer(vpolicy=Spacer.Expanding),
                await Label(self, 'InfoLbl').init(
                    text='Login'
                ), Layout.HCenter,
                Spacer(vpolicy=Spacer.Expanding),
                await Frame(self, 'EmailFrm').init(
                    layout=await Layout.vertical(self).init(
                        margins=(5, 5, 5, 5), spacing=5, alignment=Layout.Center,
                        items=[
                            await Layout.horizontal().init(
                                items=[
                                    await Label(self, 'EmailLbl').init(
                                        text='Email'
                                    ),
                                    await Button(self, 'EditBtn', False).init(
                                        text='Edit', on_click=self.execute_edit
                                    ), Layout.Right
                                ]
                            ),
                            await Input.line(self, 'EmailInp').init(
                                placeholder='address@domain.tld'
                            )
                        ]
                    )
                ), Layout.HCenter,
                await Frame(self, 'PasswordFrm', False).init(
                    layout=await Layout.vertical(self).init(
                        margins=(5, 5, 5, 5), spacing=5, alignment=Layout.Center,
                        items=[
                            await Label(self, 'PasswordLbl').init(
                                text='Password'
                            ),
                            await Input.line(self, 'PasswordInp').init(
                                placeholder='password', hidden=True
                            )
                        ]
                    )
                ), Layout.HCenter,
                await DurationLabel(self, 'ErrorLbl').init(
                    wrap=True, alignment=Layout.Center
                ), Layout.Center,
                await Button(self, 'TextBtn').init(
                    text='Don\'t have an account?', on_click=lambda: CONTEXT.CentralWidget.setCurrentIndex(1)
                ), Layout.HCenter,
                await Button(self, 'ContinueBtn').init(
                    text='Continue', on_click=self.continue_log_in
                ), Layout.HCenter,
                await Button(self, 'LogInBtn', False).init(
                    text='Log In', on_click=self.log_in
                ), Layout.HCenter,
                Spacer(vpolicy=Spacer.Expanding),
            ]
        ))
        return self

    def keyPressEvent(self, event: QKeyEvent) -> None:
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            if self.ContinueBtn.isVisible():
                self.ContinueBtn.click()
            elif self.LogInBtn.isVisible():
                self.LogInBtn.click()
        super().keyPressEvent(event)

    @asyncSlot()
    async def execute_edit(self):
        self.PasswordFrm.setVisible(False)
        self.EditBtn.setVisible(False)
        self.EmailInp.setEnabled(True)
        self.ContinueBtn.setVisible(True)
        self.LogInBtn.setVisible(False)

    @asyncSlot()
    async def continue_log_in(self):
        email = self.EmailInp.text()
        if not len(email):
            return self.ErrorLbl.setText('Email can not be empty')
        if not await api.check_email(email):
            return self.ErrorLbl.setText(f'Email is not registered')
        self.PasswordFrm.setVisible(True)
        self.EditBtn.setVisible(True)
        self.EmailInp.setEnabled(False)
        self.ContinueBtn.setVisible(False)
        self.LogInBtn.setVisible(True)

    @asyncSlot()
    async def log_in(self):
        email = self.EmailInp.text()
        password = self.PasswordInp.text()
        if not len(password):
            return self.ErrorLbl.setText('Password can not be empty')
        current_user = await api.login({'email': email, 'password': password})
        if not (token := current_user.get('access_token')):
            return self.ErrorLbl.setText('Internal error, please try again')
        CONTEXT.CentralWidget.setCurrentWidget(CONTEXT.MainView)
        self.EmailInp.setText('')
        self.PasswordInp.setText('')
        await self.execute_edit()
