from PyQt5.QtGui import QFontMetrics
from PyQt5.QtWidgets import QLabel, QWidget, QSizePolicy
from PyQt5.QtCore import Qt, QSize

from ..misc import Icon
from ._wrapper import Wrapper


class Label(Wrapper, QLabel):
    def __init__(self, parent: QWidget, name: str, visible: bool = True):
        QLabel.__init__(self, parent)
        Wrapper.__init__(self, parent, name, visible)

    def paintEvent(self, event):
        if self.property('elided'):
            self.setText(QFontMetrics(self.font()).elidedText(self.text(), Qt.ElideRight, self.width() - 10))
        super().paintEvent(event)

    def init(
            self, *,
            text: str = '', alignment: Qt.Alignment = None, wrap: bool = False, size: QSize = None,
            icon: Icon = None, elided: bool = False, policy: tuple[QSizePolicy, QSizePolicy] = None
    ) -> 'Label':
        self.setText(text)
        self.setProperty('elided', elided)
        self.setWordWrap(wrap)
        if size:
            self.setFixedSize(size)
        if alignment:
            self.setAlignment(alignment)
        if icon:
            self.setPixmap(icon.icon.pixmap(icon.size))
        if policy:
            self.setSizePolicy(policy[0], policy[1])
        return self
