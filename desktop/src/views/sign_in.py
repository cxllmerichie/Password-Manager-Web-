from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QLabel, QFrame
from PyQt5.QtCore import Qt

from ..css import sign_in
from ..widgets import Button, Label, LInput


class SignIn(QWidget):
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self.setObjectName(self.__class__.__name__)
        self.setStyleSheet(sign_in.css)
        self.setAttribute(Qt.WA_StyledBackground, True)

    async def input_frame(self, label: QLabel, field: QLineEdit) -> QFrame:
        frame = QFrame(self)
        frame.setObjectName('SignInInputFrame')
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
            await Label(self).init('Email', 'SignInInputLabel'),
            await LInput(self).init('address@domain', 'SignInInputField'),
        ), alignment=Qt.AlignHCenter)
        vbox.addWidget(await self.input_frame(
            await Label(self).init('Password', 'SignInInputLabel'),
            await LInput(self).init('password', 'SignInInputField', password=True),
        ), alignment=Qt.AlignHCenter)
        vbox.addWidget(await Button(self).init(
            'Don\'t have an account?', 'SignInDontHaveBtn', lambda: self.parent().setCurrentIndex(1)
        ), alignment=Qt.AlignHCenter)
        vbox.addWidget(await Button(self).init(
            'Login', 'SignInBtn', lambda: self.parent().setCurrentIndex(2)
        ), alignment=Qt.AlignHCenter)
        return vbox

    async def init(self):
        self.setLayout(await self.__layout())
        return self
