from PyQt5.QtWidgets import QWidget, QPushButton, QLineEdit, QLabel, QSizePolicy, QFrame
from PyQt5.QtCore import Qt
from contextlib import suppress

from ..css import sign_in
from ..widgets import Button, Label, LInput, Frame, VLayout, Spacer, HLayout
from ..misc import Icons, API


class SignIn(QWidget):
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self.setObjectName(self.__class__.__name__)
        self.setStyleSheet(sign_in.css)
        self.setAttribute(Qt.WA_StyledBackground, True)

    async def __layout(self):
        vbox = await VLayout().init(spacing=10, alignment=Qt.AlignVCenter)
        vbox.addWidget(await Button(self, 'AuthExitBtn').init(
            icon=Icons.CROSS, slot=self.app.close
        ), alignment=VLayout.RightTop)
        vbox.addItem(Spacer(QSizePolicy.Minimum, QSizePolicy.Expanding))

        layout_email = await VLayout(self).init(margins=(5, 5, 5, 5), spacing=5, alignment=VLayout.CenterCenter)
        layout_email_labelbtn = await HLayout().init()
        layout_email_labelbtn.addWidget(await Label(self, 'SignInInputLabel').init(text='Email'))
        layout_email_labelbtn.addWidget(await Button(self, 'SignInInputLabelBtn').init(
            text='Edit', slot=self.edit
        ), alignment=HLayout.Right)
        layout_email.addLayout(layout_email_labelbtn)
        layout_email.addWidget(await LInput(self, 'SignInInputFieldEmail').init(placeholder='address@domain.tld'))
        vbox.addWidget(await Frame(self, 'SignInInputFrame').init(
            layout=layout_email
        ), alignment=Qt.AlignHCenter)

        layout_password = await VLayout(self).init(margins=(5, 5, 5, 5), spacing=5, alignment=VLayout.CenterCenter)
        layout_password.addWidget(await Label(self, 'SignInInputLabel').init(text='Password'))
        layout_password.addWidget(await LInput(self, 'SignInInputFieldPassword').init(placeholder='password', hidden=True))
        vbox.addWidget(await Frame(self, 'SignInInputFramePassword').init(
            layout=layout_password
        ), alignment=Qt.AlignHCenter)

        vbox.addWidget(await Label(self, 'SignInErrorLbl').init(wrap=True), alignment=VLayout.CenterCenter)
        vbox.addWidget(await Button(self, 'SignInDontHaveBtn').init(
            text='Don\'t have an account?', slot=lambda: self.parent().setCurrentIndex(1)
        ), alignment=Qt.AlignHCenter)
        vbox.addWidget(await Button(self, 'SignInBtn').init(
            text='Continue', slot=self.continue_
        ), alignment=Qt.AlignHCenter)
        vbox.addItem(Spacer(QSizePolicy.Minimum, QSizePolicy.Expanding))
        self.findChild(QFrame, 'SignInInputFramePassword').setVisible(False)
        self.findChild(QPushButton, 'SignInInputLabelBtn').setVisible(False)
        return vbox

    def edit(self):
        self.findChild(QFrame, 'SignInInputFramePassword').setVisible(False)
        self.findChild(QPushButton, 'SignInInputLabelBtn').setVisible(False)
        self.findChild(QLineEdit, 'SignInInputFieldEmail').setEnabled(True)
        sign_in_btn = self.findChild(QPushButton, 'SignInBtn')
        with suppress(Exception):
            sign_in_btn.clicked.disconnect()
        sign_in_btn.clicked.connect(self.continue_)
        sign_in_btn.setText('Continue')

    def continue_(self):
        email = self.findChild(QLineEdit, 'SignInInputFieldEmail').text()
        error_lbl = self.findChild(QLabel, 'SignInErrorLbl')
        if not len(email):
            return error_lbl.setText('Email can not be empty')
        if not API.check_email(email):
            return error_lbl.setText(f'Email is not registered')
        self.findChild(QFrame, 'SignInInputFramePassword').setVisible(True)
        self.findChild(QPushButton, 'SignInInputLabelBtn').setVisible(True)
        self.findChild(QLineEdit, 'SignInInputFieldEmail').setEnabled(False)
        sign_in_btn = self.findChild(QPushButton, 'SignInBtn')
        with suppress(Exception):
            sign_in_btn.clicked.disconnect()
        sign_in_btn.clicked.connect(self.log_in)
        sign_in_btn.setText('Log in')

    def log_in(self):
        email = self.findChild(QLineEdit, 'SignInInputFieldEmail').text()
        password = self.findChild(QLineEdit, 'SignInInputFieldPassword').text()
        error_lbl = self.findChild(QLabel, 'SignInErrorLbl')
        if not len(password):
            return error_lbl.setText('Password can not be empty')
        response = API.login(dict(email=email, password=password))
        if not (token := response.get('access_token', None)):
            return error_lbl.setText('Internal error, please try again')
        self.app.settings.setValue('token', token)
        self.parent().setCurrentIndex(2)

    @property
    def app(self):
        return self.parent().parent()

    async def init(self):
        self.setLayout(await self.__layout())
        return self
