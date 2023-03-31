from PyQt5.QtWidgets import QWidget, QLineEdit, QLabel, QSizePolicy
from PyQt5.QtCore import Qt

from ..css import sign_in
from ..widgets import Button, Label, LInput, Frame, VLayout, Spacer
from ..const import Icons


class SignIn(QWidget):
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self.setObjectName(self.__class__.__name__)
        self.setStyleSheet(sign_in.css)
        self.setAttribute(Qt.WA_StyledBackground, True)

    async def input_frame(self, label: QLabel, field: QLineEdit) -> Frame:
        vlayout = await VLayout(self).init(margins=(5, 5, 5, 5), spacing=5, alignment=VLayout.CenterCenter)
        vlayout.addWidget(label)
        vlayout.addWidget(field)
        return await Frame(self, 'SignInInputFrame').init(layout=vlayout)

    async def __layout(self):
        vbox = await VLayout().init(spacing=10, alignment=Qt.AlignVCenter)
        vbox.addWidget(await Button(self, 'AuthExitBtn').init(
            icon=Icons.CROSS, slot=self.app.close
        ), alignment=VLayout.RightTop)
        vbox.addItem(Spacer(QSizePolicy.Minimum, QSizePolicy.Expanding))
        vbox.addWidget(await self.input_frame(
            await Label(self, 'SignInInputLabel').init(text='Email'),
            await LInput(self, 'SignInInputField').init(placeholder='address@domain'),
        ), alignment=Qt.AlignHCenter)
        vbox.addWidget(await self.input_frame(
            await Label(self, 'SignInInputLabel').init(text='Password'),
            await LInput(self, 'SignInInputField').init(placeholder='password', hidden=True),
        ), alignment=Qt.AlignHCenter)
        vbox.addWidget(await Button(self, 'SignInDontHaveBtn').init(
            text='Don\'t have an account?', slot=lambda: self.parent().setCurrentIndex(1)
        ), alignment=Qt.AlignHCenter)
        vbox.addWidget(await Button(self, 'SignInBtn').init(
            text='Login', slot=lambda: self.parent().setCurrentIndex(2)
        ), alignment=Qt.AlignHCenter)
        vbox.addItem(Spacer(QSizePolicy.Minimum, QSizePolicy.Expanding))
        return vbox

    @property
    def app(self):
        return self.parent().parent()

    async def init(self):
        self.setLayout(await self.__layout())
        return self
