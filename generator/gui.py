from PyQt5.QtCore import QSize, QMargins, Qt
from PyQt5.QtWidgets import QVBoxLayout, QCheckBox, QWidget, QPushButton, QHBoxLayout, QTextEdit, QLabel
from PyQt5.QtGui import QFont, QIcon

from generator import PasswordGenerator


class Application(QWidget):
    def __init__(self):
        super(Application, self).__init__()
        self.setLayout(self.__layout())

        self.initui()

    def initui(self):
        self.setFixedSize(QSize(500, 150))
        self.setWindowTitle('Password Generator')
        self.setWindowIcon(QIcon('assets/icon-black.ico'))
        self.show()

    def font(self):
        return QFont("Times", 10, QFont.Bold)

    def checkbox(self, text: str):
        box = QCheckBox(self)
        box.setMinimumWidth(75)
        box.setFixedHeight(26)
        box.setChecked(True)
        box.setText(text)
        box.setFont(self.font())
        box.setObjectName(text.lower())
        return box

    def button(self, text: str, action):
        btn = QPushButton(self)
        btn.setText(text)
        btn.setFont(self.font())
        btn.setFixedHeight(35)
        btn.clicked.connect(action)
        return btn

    def generate(self):
        uppercase = self.findChild(QCheckBox, 'uppercase').isChecked()
        lowercase = self.findChild(QCheckBox, 'lowercase').isChecked()
        digits = self.findChild(QCheckBox, 'digits').isChecked()
        special = self.findChild(QCheckBox, 'special').isChecked()
        length = self.findChild(QTextEdit, 'length').toPlainText()
        if not any([uppercase, lowercase, digits, special]):
            return self.findChild(QLabel).setText('At least one option must be chosen.')
        try:
            length = min(max(int(length), 5), 50)
        except Exception:
            return self.findChild(QLabel).setText('Invalid length (min=5, max=50).')
        self.findChild(QLabel).setText('')
        password = str(PasswordGenerator(length, uppercase, lowercase, digits, special))
        self.findChild(QTextEdit, 'password').setText(password)

    def error(self, text):
        lbl = QLabel(self)
        lbl.setFont(self.font())
        lbl.setStyleSheet('color: red;')
        lbl.setText(text)
        lbl.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        return lbl

    def textinput(self, placeholder: str, size: QSize = QSize(100, 26), is_sized: bool = True, default: str = ''):
        txtinput = QTextEdit(self)
        txtinput.setFixedSize(size) if is_sized else txtinput.setFixedHeight(size.height())
        txtinput.setObjectName(placeholder.lower())
        txtinput.setFont(self.font())
        txtinput.setPlaceholderText(placeholder)
        txtinput.setText(default)
        return txtinput

    def __layout(self):
        vbox = QVBoxLayout()
        hbox = QHBoxLayout()
        hbox.setSpacing(0)
        hbox.setContentsMargins(QMargins(0, 0, 0, 0))
        hbox.addWidget(self.checkbox('Uppercase'))
        hbox.addWidget(self.checkbox('Lowercase'))
        hbox.addWidget(self.checkbox('Digits'))
        hbox.addWidget(self.checkbox('Special'))
        hbox.addWidget(self.textinput('Length', default='20'))
        vbox.addLayout(hbox)
        vbox.addWidget(self.textinput('Password', QSize(0, 26), False))
        vbox.addWidget(self.error(''))
        vbox.addWidget(self.button('Generate', self.generate))
        return vbox
