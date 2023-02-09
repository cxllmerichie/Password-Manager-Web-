from PyQt5.QtCore import QSize, QMargins
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QTextEdit


class Item(QWidget):
    def __init__(self, key, value):
        super(Item, self).__init__()
        self.setObjectName(key)
        self.setLayout(self.__layout(key ,value))

    def __layout(self, key, value):
        hbox = QHBoxLayout()
        hbox.setSpacing(0)
        hbox.setContentsMargins(QMargins(0, 0, 0, 0))
        hbox.addWidget(self.__textedit(QSize(100, 26), key, 'Key'))
        hbox.addWidget(self.__textedit(QSize(300, 26), value, 'Value'))
        return hbox

    def font(self):
        return QFont('Times', 10)

    def __textedit(self, size: QSize, text: str, name: str):
        textedit = QTextEdit(self)
        textedit.setObjectName(name)
        textedit.resize(size)
        textedit.setMaximumHeight(26)
        textedit.setFont(self.font())
        textedit.setText(text)
        return textedit