from qcontextapi.widgets import Button, Label, LineInput, Frame, Layout, Spacer, Widget
from qcontextapi import CONTEXT
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt, pyqtSlot

from ..misc import ICONS, API
from .view_main import MainView
from .. import css


class SignIn(Widget):
    def __init__(self, parent: QWidget):
        super().__init__(parent, self.__class__.__name__, stylesheet=css.view_signin.css)

    def init(self) -> 'SignIn':
        self.setLayout(
            Layout.vertical().init(
                spacing=10, alignment=Qt.AlignVCenter,
                items=[
                    Button(self, 'AuthExitBtn').init(
                        icon=ICONS.CROSS, slot=self.parent().parent().close
                    ), Layout.RightTop,
                    Spacer(False, True),
                    Label(self, 'InfoLbl').init(
                        text='Login'
                    ), Layout.HCenter,
                    Spacer(False, True),
                    Frame(self, 'InputFrameEmail').init(
                        layout=Layout.vertical(self).init(
                            margins=(5, 5, 5, 5), spacing=5, alignment=Layout.Center,
                            items=[
                                Layout.horizontal().init(
                                    items=[
                                        Label(self, 'InputLabelEmail').init(
                                            text='Email'
                                        ),
                                        Button(self, 'InputLabelEmailEditBtn', False).init(
                                            text='Edit', slot=self.edit
                                        ), Layout.Right
                                    ]
                                ),
                                LineInput(self, 'InputFieldEmail').init(
                                    placeholder='address@domain.tld'
                                )
                            ]
                        )
                    ), Qt.AlignHCenter,
                    Frame(self, 'InputFramePassword', False).init(
                        layout=Layout.vertical(self).init(
                            margins=(5, 5, 5, 5), spacing=5, alignment=Layout.Center,
                            items=[
                                Label(self, 'InputLabelPassword').init(
                                    text='Password'
                                ),
                                LineInput(self, 'InputFieldPassword').init(
                                    placeholder='password', hidden=True
                                )
                            ]
                        )
                    ), Qt.AlignHCenter,
                    Label(self, 'ErrorLbl').init(
                        wrap=True, alignment=Layout.Center
                    ), Layout.Center,
                    Button(self, 'AuthTextBtn').init(
                        text='Don\'t have an account?', slot=lambda: CONTEXT.CentralWidget.setCurrentIndex(1)
                    ), Qt.AlignHCenter,
                    Button(self, 'ContinueBtn').init(
                        text='Continue', slot=self.continue_log_in
                    ), Qt.AlignHCenter,
                    Button(self, 'LogInBtn', False).init(
                        text='Log In', slot=self.log_in
                    ), Qt.AlignHCenter,
                    Spacer(False, True)
                ]
            )
        )
        return self

    @pyqtSlot()
    def edit(self):
        self.InputFramePassword.setVisible(False)
        self.InputLabelEmailEditBtn.setVisible(False)
        self.InputFieldEmail.setEnabled(True)
        self.ContinueBtn.setVisible(True)
        self.LogInBtn.setVisible(False)

    @pyqtSlot()
    def continue_log_in(self):
        email = self.InputFieldEmail.text()
        if not len(email):
            return self.ErrorLbl.setText('Email can not be empty')
        if not API.check_email(email):
            return self.ErrorLbl.setText(f'Email is not registered')
        self.InputFramePassword.setVisible(True)
        self.InputLabelEmailEditBtn.setVisible(True)
        self.InputFieldEmail.setEnabled(False)
        self.ContinueBtn.setVisible(False)
        self.LogInBtn.setVisible(True)

    @pyqtSlot()
    def log_in(self):
        email = self.InputFieldEmail.text()
        password = self.InputFieldPassword.text()
        if not len(password):
            return self.ErrorLbl.setText('Password can not be empty')
        user = {'email': email, 'password': password}
        if not (token := API.login(user).get('access_token')):
            return self.ErrorLbl.setText('Internal error, please try again')
        CONTEXT.token = token
        CONTEXT.CentralWidget.addWidget(widget := MainView(self).init())
        CONTEXT.CentralWidget.setCurrentWidget(widget)
