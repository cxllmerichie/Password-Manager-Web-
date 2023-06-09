from aioqui.widgets import Button, Label, Input, Layout, Spacer, Frame, Widget, Parent
from aioqui.widgets.custom import DurationLabel
from aioqui.asynq import asyncSlot
from aioqui import CONTEXT
import email_validator

from ..misc import ICONS, API
from .. import qss


class SignUp(Widget):
    def __init__(self, parent: Parent):
        super().__init__(parent, self.__class__.__name__, qss=qss.view_signup.css)

    async def init(self) -> 'SignUp':
        self.setLayout(await Layout.vertical().init(
            spacing=10, alignment=Layout.VCenter,
            items=[
                await Button(self, 'AuthExitBtn').init(
                    icon=ICONS.CROSS, on_click=self.core.close
                ), Layout.RightTop,
                Spacer(Spacer.Minimum, Spacer.Expanding),
                await Label(self, 'InfoLbl').init(
                    text='Registration'
                ), Layout.HCenter,
                Spacer(Spacer.Minimum, Spacer.Expanding),
                await Frame(self, 'InputFrameEmail').init(
                    layout=await Layout.vertical(self).init(
                        margins=(5, 5, 5, 5), spacing=5, alignment=Layout.Center,
                        items=[
                            await Label(self, 'InputLabelEmail').init(
                                text='Email'
                            ),
                            await Input.line(self, 'InputFieldEmail').init(
                                placeholder='address@domain.tld', on_change=self.validate_email
                            )
                        ]
                    )
                ), Layout.HCenter,
                await Frame(self, 'InputFramePassword').init(
                    layout=await Layout.vertical(self).init(
                        margins=(5, 5, 5, 5), spacing=5, alignment=Layout.Center,
                        items=[
                            await Label(self, 'InputLabelPassword').init(
                                text='Password'
                            ),
                            await Input.line(self, 'InputFieldPassword').init(
                                placeholder='password', hidden=True, on_change=self.validate_password
                            )
                        ]
                    )
                ), Layout.HCenter,
                await Frame(self, 'InputFrameConfpass').init(
                    layout=await Layout.vertical(self).init(
                        margins=(5, 5, 5, 5), spacing=5, alignment=Layout.Center,
                        items=[
                            await Label(self, 'InputLabelConfpass').init(
                                text='Confirm password'
                            ),
                            await Input.line(self, 'InputFieldConfpass').init(
                                placeholder='password', hidden=True, on_change=self.validate_confpass
                            )
                        ]
                    )
                ), Layout.HCenter,
                await DurationLabel(self, 'ErrorLbl').init(
                    wrap=True, alignment=Layout.Center
                ), Layout.Center,
                await Button(self, 'AuthTextBtn').init(
                    text='Already have an account?', on_click=lambda: CONTEXT.CentralWidget.setCurrentIndex(0)
                ), Layout.HCenter,
                await Button(self, 'AuthMainBtn').init(
                    text='Create Account', on_click=self.sign_up
                ), Layout.HCenter,
                Spacer(Spacer.Minimum, Spacer.Expanding)
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
        CONTEXT.CentralWidget.setCurrentWidget(CONTEXT.MainView)
