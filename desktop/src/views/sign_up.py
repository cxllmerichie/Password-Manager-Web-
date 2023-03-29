from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QLabel, QFrame, QPushButton
from PyQt5.QtCore import QSize, Qt, QObject

from ..css import sign_up


class SignUp(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.setObjectName(self.__class__.__name__)
        self.setStyleSheet(sign_up.css)
        self.setAttribute(Qt.WA_StyledBackground, True)

    async def input_label(self, text: str) -> QLabel:
        lbl = QLabel(self)
        lbl.setObjectName('SignUpInputLabel')
        lbl.setText(text)
        return lbl

    async def input_field(self, placeholder: str) -> QLineEdit:
        inp = QLineEdit(self)
        inp.setObjectName('SignUpInputField')
        inp.setPlaceholderText(placeholder)
        return inp

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

    async def sign_in_btn(self, text: str) -> QPushButton:
        btn = QPushButton(self)
        btn.setObjectName('SignUpBtn')
        btn.setText(text)
        return btn

    async def __layout(self):
        vbox = QVBoxLayout()
        vbox.setContentsMargins(0, 0, 0, 0)
        vbox.setSpacing(10)
        vbox.setAlignment(Qt.AlignVCenter)
        vbox.addWidget(await self.input_frame(
            await self.input_label('Email'),
            await self.input_field('address@domen'),
        ), alignment=Qt.AlignHCenter)
        vbox.addWidget(await self.input_frame(
            await self.input_label('Password'),
            await self.input_field('password'),
        ), alignment=Qt.AlignHCenter)
        vbox.addWidget(await self.input_frame(
            await self.input_label('Confirm password'),
            await self.input_field('password'),
        ), alignment=Qt.AlignHCenter)
        vbox.addWidget(await self.sign_in_btn('Create Account'), alignment=Qt.AlignHCenter)
        return vbox

    async def init(self):
        self.setLayout(await self.__layout())
        return self
