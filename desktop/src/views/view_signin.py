from aioqui.widgets import Button, Label, Input, Frame, Layout, Spacer, Widget, Parent
from aioqui.widgets.custom import DurationLabel
from aioqui.asynq import asyncSlot
from aioqui import CONTEXT

from ..misc import ICONS, API
from .. import qss


class SignIn(Frame):
    def __init__(self, parent: Parent):
        super().__init__(parent, self.__class__.__name__, qss=qss.view_signin.css)

    async def init(self) -> 'SignIn':
        self.setLayout(await Layout.vertical().init(
            spacing=10, alignment=Layout.VCenter,
            items=[
                await Button(self, 'AuthExitBtn').init(
                    icon=ICONS.CROSS, on_click=self.core.close
                ), Layout.RightTop,
                Spacer(Spacer.Minimum, Spacer.Expanding),
                await Label(self, 'InfoLbl').init(
                    text='Login'
                ), Layout.HCenter,
                Spacer(Spacer.Minimum, Spacer.Expanding),
                await Frame(self, 'InputFrameEmail').init(
                    layout=await Layout.vertical(self).init(
                        margins=(5, 5, 5, 5), spacing=5, alignment=Layout.Center,
                        items=[
                            await Layout.horizontal().init(
                                items=[
                                    await Label(self, 'InputLabelEmail').init(
                                        text='Email'
                                    ),
                                    await Button(self, 'InputLabelEmailEditBtn', False).init(
                                        text='Edit', on_click=self.edit
                                    ), Layout.Right
                                ]
                            ),
                            await Input.line(self, 'InputFieldEmail').init(
                                placeholder='address@domain.tld'
                            )
                        ]
                    )
                ), Layout.HCenter,
                await Frame(self, 'InputFramePassword', False).init(
                    layout=await Layout.vertical(self).init(
                        margins=(5, 5, 5, 5), spacing=5, alignment=Layout.Center,
                        items=[
                            await Label(self, 'InputLabelPassword').init(
                                text='Password'
                            ),
                            await Input.line(self, 'InputFieldPassword').init(
                                placeholder='password', hidden=True
                            )
                        ]
                    )
                ), Layout.HCenter,
                await DurationLabel(self, 'ErrorLbl').init(
                    wrap=True, alignment=Layout.Center
                ), Layout.Center,
                await Button(self, 'AuthTextBtn').init(
                    text='Don\'t have an account?', on_click=lambda: CONTEXT.CentralWidget.setCurrentIndex(1)
                ), Layout.HCenter,
                await Button(self, 'ContinueBtn').init(
                    text='Continue', on_click=self.continue_log_in
                ), Layout.HCenter,
                await Button(self, 'LogInBtn', False).init(
                    text='Log In', on_click=self.log_in
                ), Layout.HCenter,
                Spacer(Spacer.Minimum, Spacer.Expanding)
            ]
        ))
        return self

    @asyncSlot()
    async def edit(self):
        self.InputFramePassword.setVisible(False)
        self.InputLabelEmailEditBtn.setVisible(False)
        self.InputFieldEmail.setEnabled(True)
        self.ContinueBtn.setVisible(True)
        self.LogInBtn.setVisible(False)

    @asyncSlot()
    async def continue_log_in(self):
        email = self.InputFieldEmail.text()
        if not len(email):
            return self.ErrorLbl.setText('Email can not be empty')
        if not await API.check_email(email):
            return self.ErrorLbl.setText(f'Email is not registered')
        self.InputFramePassword.setVisible(True)
        self.InputLabelEmailEditBtn.setVisible(True)
        self.InputFieldEmail.setEnabled(False)
        self.ContinueBtn.setVisible(False)
        self.LogInBtn.setVisible(True)

    @asyncSlot()
    async def log_in(self):
        email = self.InputFieldEmail.text()
        password = self.InputFieldPassword.text()
        if not len(password):
            return self.ErrorLbl.setText('Password can not be empty')
        current_user = await API.login({'email': email, 'password': password})
        if not (token := current_user.get('access_token')):
            return self.ErrorLbl.setText('Internal error, please try again')
        CONTEXT.CentralWidget.setCurrentWidget(CONTEXT.MainView)
