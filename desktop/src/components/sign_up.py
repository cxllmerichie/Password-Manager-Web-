from PyQt5.QtWidgets import QWidget, QLineEdit, QLabel
from PyQt5.QtCore import Qt
import email_validator

from ..css import sign_up
from ..widgets import Button, Label, LInput, VLayout, Spacer, Frame
from ..misc import Icons, api


class SignUp(QWidget):
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self.setObjectName(self.__class__.__name__)
        self.setStyleSheet(sign_up.css)
        self.setAttribute(Qt.WA_StyledBackground, True)

    async def init(self) -> 'SignUp':
        vbox = await VLayout().init(spacing=10, alignment=Qt.AlignVCenter)
        vbox.addWidget(await Button(self, 'AuthExitBtn').init(
            icon=Icons.CROSS, slot=self.app.close
        ), alignment=VLayout.RightTop)
        vbox.addItem(Spacer(False, True))

        layout_email = await VLayout(self).init(margins=(5, 5, 5, 5), spacing=5, alignment=VLayout.CenterCenter)
        layout_email.addWidget(await Label(self, 'InputLabelEmail').init(text='Email'))
        layout_email.addWidget(await LInput(self, 'InputFieldEmail').init(
            placeholder='address@domain.tld', textchanged=self.validate_email
        ))
        vbox.addWidget(await Frame(self, 'InputFrameEmail').init(
            layout=layout_email
        ), alignment=Qt.AlignHCenter)

        layout_password = await VLayout(self).init(margins=(5, 5, 5, 5), spacing=5, alignment=VLayout.CenterCenter)
        layout_password.addWidget(await Label(self, 'InputLabelPassword').init(text='Password'))
        layout_password.addWidget(await LInput(self, 'InputFieldPassword').init(
            placeholder='password', hidden=True, textchanged=self.validate_password
        ))
        vbox.addWidget(await Frame(self, 'InputFramePassword').init(
            layout=layout_password
        ), alignment=Qt.AlignHCenter)

        layout_confpass = await VLayout(self).init(margins=(5, 5, 5, 5), spacing=5, alignment=VLayout.CenterCenter)
        layout_confpass.addWidget(await Label(self, 'InputLabelConfpass').init(text='Confirm password'))
        layout_confpass.addWidget(await LInput(self, 'InputFieldConfpass').init(
            placeholder='password', hidden=True, textchanged=self.validate_confpass
        ))
        vbox.addWidget(await Frame(self, 'InputFrameConfpass').init(
            layout=layout_confpass
        ), alignment=Qt.AlignHCenter)

        vbox.addWidget(await Label(self, 'ErrorLbl').init(
            wrap=True, alignment=VLayout.CenterCenter
        ), alignment=VLayout.CenterCenter)
        vbox.addWidget(await Button(self, 'AuthTextBtn').init(
            text='Already have an account?', slot=lambda: self.parent().setCurrentIndex(0)
        ), alignment=Qt.AlignHCenter)
        vbox.addWidget(await Button(self, 'AuthMainBtn').init(
            text='Create Account', slot=self.sign_up
        ), alignment=Qt.AlignHCenter)
        vbox.addItem(Spacer(False, True))
        self.setLayout(vbox)
        return self

    def validate_email(self):
        email = self.findChild(QLineEdit, 'InputFieldEmail').text()
        error = ''
        try:
            email_validator.validate_email(email)
        except Exception as exception:
            error = str(exception)
        self.findChild(QLabel, 'ErrorLbl').setText(error)
        return len(error) == 0

    def validate_password(self):
        password = self.findChild(QLineEdit, 'InputFieldPassword').text()
        error = ''
        if len(password) < 8:
            error = 'Password length must be greater than 8'
        self.findChild(QLabel, 'ErrorLbl').setText(error)
        return len(error) == 0

    def validate_confpass(self):
        password = self.findChild(QLineEdit, 'InputFieldPassword').text()
        confpass = self.findChild(QLineEdit, 'InputFieldConfpass').text()
        error = ''
        if password != confpass:
            error = 'Password and confirmation password do not match'
        self.findChild(QLabel, 'ErrorLbl').setText(error)
        return len(error) == 0

    def sign_up(self):
        email = self.findChild(QLineEdit, 'InputFieldEmail').text()
        password = self.findChild(QLineEdit, 'InputFieldPassword').text()
        if not self.validate_email():
            return
        if not self.validate_password():
            return
        if not self.validate_confpass():
            return
        body = {'email': email, 'password': password}
        if not (token := api.create_user(body).get('access_token', None)):
            return self.findChild(QLabel, 'ErrorLbl').setText('Internal error, please try again')
        self.app.settings.setValue('token', token)
        self.parent().setCurrentIndex(2)

    @property
    def app(self):
        return self.parent().parent()
