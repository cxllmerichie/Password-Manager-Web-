from PyQt5.QtWidgets import QWidget, QPushButton, QLineEdit, QLabel, QFrame
from PyQt5.QtCore import Qt, pyqtSlot

from ..widgets import Button, Label, LineInput, Frame, Layout, Spacer
from ..misc import Icons, api
from .main_view import MainView
from .. import css


class SignIn(QWidget):
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self.setObjectName(self.__class__.__name__)
        self.setStyleSheet(css.sign_in.css)
        self.setAttribute(Qt.WA_StyledBackground, True)

    def init(self) -> 'SignIn':
        vbox = Layout.vertical().init(spacing=10, alignment=Qt.AlignVCenter)
        vbox.addWidget(Button(self, 'AuthExitBtn').init(
            icon=Icons.CROSS, slot=self.parent().parent().close
        ), alignment=Layout.RightTop)
        vbox.addItem(Spacer(False, True))

        layout_email = Layout.vertical(self).init(
            margins=(5, 5, 5, 5), spacing=5, alignment=Layout.CenterCenter
        )
        layout_email_labelbtn = Layout.horizontal().init()
        layout_email_labelbtn.addWidget(Label(self, 'InputLabelEmail').init(
            text='Email'
        ))
        layout_email_labelbtn.addWidget(edit_btn := Button(self, 'InputLabelEmailEditBtn', False).init(
            text='Edit', slot=self.edit
        ), alignment=Layout.Right)
        layout_email.addLayout(layout_email_labelbtn)
        layout_email.addWidget(LineInput(self, 'InputFieldEmail').init(
            placeholder='address@domain.tld'
        ))
        vbox.addWidget(Frame(self, 'InputFrameEmail').init(
            layout=layout_email
        ), alignment=Qt.AlignHCenter)

        layout_password = Layout.vertical(self).init(
            margins=(5, 5, 5, 5), spacing=5, alignment=Layout.CenterCenter
        )
        layout_password.addWidget(Label(self, 'InputLabelPassword').init(
            text='Password'
        ))
        layout_password.addWidget(LineInput(self, 'InputFieldPassword').init(
            placeholder='password', hidden=True
        ))

        vbox.addWidget(frame := Frame(self, 'InputFramePassword', False).init(
            layout=layout_password
        ), alignment=Qt.AlignHCenter)

        vbox.addWidget(Label(self, 'ErrorLbl').init(
            wrap=True, alignment=Layout.CenterCenter
        ), alignment=Layout.CenterCenter)
        vbox.addWidget(Button(self, 'AuthTextBtn').init(
            text='Don\'t have an account?', slot=lambda: self.parent().setCurrentIndex(1)
        ), alignment=Qt.AlignHCenter)
        vbox.addWidget(Button(self, 'ContinueBtn').init(
            text='Continue', slot=self.continue_log_in
        ), alignment=Qt.AlignHCenter)
        vbox.addWidget(log_in_btn := Button(self, 'LogInBtn', False).init(
            text='Log In', slot=self.log_in
        ), alignment=Qt.AlignHCenter)
        vbox.addItem(Spacer(False, True))
        self.setLayout(vbox)
        return self

    @pyqtSlot()
    def edit(self):
        self.findChild(QFrame, 'InputFramePassword').setVisible(False)
        self.findChild(QPushButton, 'InputLabelEmailEditBtn').setVisible(False)
        self.findChild(QLineEdit, 'InputFieldEmail').setEnabled(True)

    @pyqtSlot()
    def continue_log_in(self):
        email_input = self.findChild(QLineEdit, 'InputFieldEmail')
        email = email_input.text()
        error_lbl = self.findChild(QLabel, 'ErrorLbl')
        if not len(email):
            return error_lbl.setText('Email can not be empty')
        if not api.check_email(email):
            return error_lbl.setText(f'Email is not registered')
        self.findChild(QFrame, 'InputFramePassword').setVisible(True)
        self.findChild(QPushButton, 'InputLabelEmailEditBtn').setVisible(True)
        email_input.setEnabled(False)
        self.findChild(QPushButton, 'ContinueBtn').setVisible(False)
        self.findChild(QPushButton, 'LogInBtn').setVisible(True)

    @pyqtSlot()
    def log_in(self):
        email = self.findChild(QLineEdit, 'InputFieldEmail').text()
        password = self.findChild(QLineEdit, 'InputFieldPassword').text()
        error_lbl = self.findChild(QLabel, 'ErrorLbl')
        if not len(password):
            return error_lbl.setText('Password can not be empty')
        if not (token := api.login(dict(email=email, password=password)).get('access_token', None)):
            return error_lbl.setText('Internal error, please try again')
        api.CONFIG.setValue('token', token)
        self.parent().addWidget(MainView(self.parent()).init())
        self.parent().setCurrentIndex(2)
