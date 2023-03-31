from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QLabel, QFrame, QSizePolicy
from PyQt5.QtCore import Qt

from ..css import sign_up
from ..widgets import Button, Label, LInput, VLayout, Spacer
from ..assets import Icons


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
        vbox = await VLayout().init(spacing=10, alignment=Qt.AlignVCenter)
        vbox.addWidget(await Button(self, 'AuthExitBtn').init(
            icon=Icons.CROSS, slot=self.app.close
        ), alignment=VLayout.RightTop)
        vbox.addItem(Spacer(QSizePolicy.Minimum, QSizePolicy.Expanding))
        vbox.addWidget(await self.input_frame(
            await Label(self, 'SignUpInputLabel').init(text='Email'),
            await LInput(self, 'SignUpInputField').init(placeholder='address@domain'),
        ), alignment=Qt.AlignHCenter)
        vbox.addWidget(await self.input_frame(
            await Label(self, 'SignUpInputLabel').init(text='Password'),
            await LInput(self, 'SignUpInputField').init(placeholder='password', hidden=True),
        ), alignment=Qt.AlignHCenter)
        vbox.addWidget(await self.input_frame(
            await Label(self, 'SignUpInputLabel').init(text='Confirm password'),
            await LInput(self, 'SignUpInputField').init(placeholder='password', hidden=True),
        ), alignment=Qt.AlignHCenter)
        vbox.addWidget(await Button(self, 'SignUpAlreadyHaveBtn').init(
            text='Already have an account?', slot=lambda: self.parent().setCurrentIndex(0)
        ), alignment=Qt.AlignHCenter)
        vbox.addWidget(await Button(self, 'SignUpBtn').init(
            text='Create Account'
        ), alignment=Qt.AlignHCenter)
        vbox.addItem(Spacer(QSizePolicy.Minimum, QSizePolicy.Expanding))
        return vbox

    @property
    def app(self):
        return self.parent().parent()

    async def init(self):
        self.setLayout(await self.__layout())
        return self
