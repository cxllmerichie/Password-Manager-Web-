from qcontextapi.widgets import Button, Label, LineInput, Layout, Spacer, Frame, Widget
from qcontextapi import CONTEXT
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt, pyqtSlot
import email_validator

from ..misc import ICONS, api_remote
from .view_main import MainView
from .. import css


class SignUp(Widget):
    def __init__(self, parent: QWidget):
        super().__init__(parent, self.__class__.__name__, stylesheet=css.view_signup.css)

    def init(self) -> 'SignUp':
        self.setLayout(
            Layout.vertical().init(
                spacing=10, alignment=Qt.AlignVCenter,
                items=[
                    Button(self, 'AuthExitBtn').init(
                        icon=ICONS.CROSS, slot=self.parent().parent().close
                    ), Layout.RightTop,
                    Spacer(False, True),
                    Label(self, 'InfoLbl').init(
                        text='Registration'
                    ), Layout.HCenter,
                    Spacer(False, True),
                    Frame(self, 'InputFrameEmail').init(
                        layout=Layout.vertical(self).init(
                            margins=(5, 5, 5, 5), spacing=5, alignment=Layout.Center,
                            items=[
                                Label(self, 'InputLabelEmail').init(
                                    text='Email'
                                ),
                                LineInput(self, 'InputFieldEmail').init(
                                    placeholder='address@domain.tld', textchanged=self.validate_email
                                )
                            ]
                        )
                    ), Qt.AlignHCenter,
                    Frame(self, 'InputFramePassword').init(
                        layout=Layout.vertical(self).init(
                            margins=(5, 5, 5, 5), spacing=5, alignment=Layout.Center,
                            items=[
                                Label(self, 'InputLabelPassword').init(
                                    text='Password'
                                ),
                                LineInput(self, 'InputFieldPassword').init(
                                    placeholder='password', hidden=True, textchanged=self.validate_password
                                )
                            ]
                        )
                    ), Qt.AlignHCenter,
                    Frame(self, 'InputFrameConfpass').init(
                        layout=Layout.vertical(self).init(
                            margins=(5, 5, 5, 5), spacing=5, alignment=Layout.Center,
                            items=[
                                Label(self, 'InputLabelConfpass').init(
                                    text='Confirm password'
                                ),
                                LineInput(self, 'InputFieldConfpass').init(
                                    placeholder='password', hidden=True, textchanged=self.validate_confpass
                                )
                            ]
                        )
                    ), Qt.AlignHCenter,
                    Label(self, 'ErrorLbl').init(
                        wrap=True, alignment=Layout.Center
                    ), Layout.Center,
                    Button(self, 'AuthTextBtn').init(
                        text='Already have an account?', slot=lambda: CONTEXT.CentralWidget.setCurrentIndex(0)
                    ), Qt.AlignHCenter,
                    Button(self, 'AuthMainBtn').init(
                        text='Create Account', slot=self.sign_up
                    ), Qt.AlignHCenter,
                    Spacer(False, True)
                ]
            )
        )
        return self

    def validate_email(self):
        error = ''
        try:
            email_validator.validate_email(self.InputFieldEmail.text())
        except Exception as exception:
            error = str(exception)
        self.ErrorLbl.setText(error)
        return len(error) == 0

    def validate_password(self):
        error = ''
        if len(self.InputFieldPassword.text()) < 8:
            error = 'Password length must be greater than 8'
        self.ErrorLbl.setText(error)
        return len(error) == 0

    def validate_confpass(self):
        error = ''
        if self.InputFieldPassword.text() != self.InputFieldConfpass.text():
            error = 'Password and confirmation password do not match'
        self.ErrorLbl.setText(error)
        return len(error) == 0

    @pyqtSlot()
    def sign_up(self):
        if not self.validate_email():
            return
        if not self.validate_password():
            return
        if not self.validate_confpass():
            return
        user = {'email': self.InputFieldEmail.text(), 'password': self.InputFieldPassword.text()}
        if not (token := api.create_user(user).get('access_token')):
            return self.ErrorLbl.setText('Internal error, please try again')
        api.set_token(token)
        CONTEXT.CentralWidget.addWidget(widget := MainView(self).init())
        CONTEXT.CentralWidget.setCurrentWidget(widget)
