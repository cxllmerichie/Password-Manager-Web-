from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QLabel, QFrame
from PyQt5.QtCore import Qt

from ..css import sign_up
from ..widgets import Button, Label, LInput


class SignUp(QWidget):
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self.setObjectName(self.__class__.__name__)
        self.setStyleSheet(sign_up.css)
        self.setAttribute(Qt.WA_StyledBackground, True)

    async def input_frame(self, label: QLabel, field: QLineEdit) -> QFrame:
        frame = QFrame(self)
        frame.setObjectName('SignUpInputFrame')
        vbox = QVBoxLayout(frame)
        vbox.setContentsMargins(5, 5, 5, 5)
        vbox.setSpacing(5)
        vbox.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        vbox.addWidget(label)
        vbox.addWidget(field)
        frame.setLayout(vbox)
        return frame

    async def __layout(self):
        vbox = QVBoxLayout()
        vbox.setContentsMargins(0, 0, 0, 0)
        vbox.setSpacing(10)
        vbox.setAlignment(Qt.AlignVCenter)
        vbox.addWidget(await self.input_frame(
            await Label(self).init('Email', 'SignUpInputLabel'),
            await LInput(self).init('address@domain', 'SignUpInputField'),
        ), alignment=Qt.AlignHCenter)
        vbox.addWidget(await self.input_frame(
            await Label(self).init('Password', 'SignUpInputLabel'),
            await LInput(self).init('password', 'SignUpInputField', hidden=True),
        ), alignment=Qt.AlignHCenter)
        vbox.addWidget(await self.input_frame(
            await Label(self).init('Confirm password', 'SignUpInputLabel'),
            await LInput(self).init('password', 'SignUpInputField', hidden=True),
        ), alignment=Qt.AlignHCenter)
        vbox.addWidget(await Button(self, 'SignUpAlreadyHaveBtn').init(
            text='Already have an account?', slot=lambda: self.parent().setCurrentIndex(0)
        ), alignment=Qt.AlignHCenter)
        vbox.addWidget(await Button(self, 'SignUpBtn').init(
            text='Create Account'
        ), alignment=Qt.AlignHCenter)
        return vbox

    async def init(self):
        self.setLayout(await self.__layout())
        return self
