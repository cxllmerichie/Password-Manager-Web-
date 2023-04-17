from PyQt5.QtGui import QFontMetrics
from PyQt5.QtWidgets import QLabel, QWidget
from PyQt5.QtCore import Qt, QSize

from ..misc import Icon, Size
from ._wrapper import Wrapper


class Label(QLabel, Wrapper):
    def __init__(self, parent: QWidget, name: str, visible: bool = True):
        QLabel.__init__(self, parent)
        Wrapper.__init__(self, parent, name, visible)

    def init(
            self, *,
            text: str = '', alignment: Qt.Alignment = None, wrap: bool = False,
            icon: Icon = None, elided: bool = False
    ) -> 'Label':
        self.setText(text)
        self.setProperty('elided', elided)
        self.setWordWrap(wrap)
        if alignment:
            self.setAlignment(alignment)
        if icon:
            self.setPixmap(icon.icon.pixmap(icon.size))
        return self

    def paintEvent(self, event):
        if self.property('elided'):
            self.setText(QFontMetrics(self.font()).elidedText(self.text(), Qt.ElideRight, self.width() - 10))
        super().paintEvent(event)
