from qcontext.widgets import Button, Label, LineInput, Frame, Layout, Spacer, Widget
from qcontext.widgets.custom import ErrorLabel
from qcontext.qasyncio import asyncSlot
from qcontext import CONTEXT
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt

from ..misc import ICONS, API
from .. import stylesheets


class SignIn(Widget):
    def __init__(self, parent: QWidget):
        super().__init__(parent, self.__class__.__name__, stylesheet=stylesheets.view_signin.css)

    async def init(self) -> 'SignIn':
        self.setLayout(await Layout.vertical().init(
            spacing=10, alignment=Qt.AlignVCenter,
            items=[
                await Button(self, 'AuthExitBtn').init(
                    icon=ICONS.CROSS, slot=self.core.close
                ), Layout.RightTop,
                Spacer(False, True),
                await Label(self, 'InfoLbl').init(
                    text='Login'
                ), Layout.HCenter,
                Spacer(False, True),
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
                                        text='Edit', slot=self.edit
                                    ), Layout.Right
                                ]
                            ),
                            await LineInput(self, 'InputFieldEmail').init(
                                placeholder='address@domain.tld'
                            )
                        ]
                    )
                ), Qt.AlignHCenter,
                await Frame(self, 'InputFramePassword', False).init(
                    layout=await Layout.vertical(self).init(
                        margins=(5, 5, 5, 5), spacing=5, alignment=Layout.Center,
                        items=[
                            await Label(self, 'InputLabelPassword').init(
                                text='Password'
                            ),
                            await LineInput(self, 'InputFieldPassword').init(
                                placeholder='password', hidden=True
                            )
                        ]
                    )
                ), Qt.AlignHCenter,
                await ErrorLabel(self, 'ErrorLbl').init(
                    wrap=True, alignment=Layout.Center
                ), Layout.Center,
                await Button(self, 'AuthTextBtn').init(
                    text='Don\'t have an account?', slot=lambda: CONTEXT.CentralWidget.setCurrentIndex(1)
                ), Qt.AlignHCenter,
                await Button(self, 'ContinueBtn').init(
                    text='Continue', slot=self.continue_log_in
                ), Qt.AlignHCenter,
                await Button(self, 'LogInBtn', False).init(
                    text='Log In', slot=self.log_in
                ), Qt.AlignHCenter,
                Spacer(False, True)
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
        await CONTEXT.LeftMenu.refresh_categories(await API.get_categories())
        CONTEXT.CentralWidget.setCurrentWidget(CONTEXT.MainView)
