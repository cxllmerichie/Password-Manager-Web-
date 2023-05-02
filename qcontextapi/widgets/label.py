from PyQt5.QtGui import QFontMetrics, QPaintEvent
from PyQt5.QtWidgets import QLabel, QWidget, QSizePolicy
from PyQt5.QtCore import Qt, QSize

from ..misc import Icon
from ..extensions import ContextObjectExt


class Label(ContextObjectExt, QLabel):
    elided = False
    non_elided_text = ''

    def __init__(self, parent: QWidget, name: str, visible: bool = True):
        QLabel.__init__(self, parent)
        ContextObjectExt.__init__(self, parent, name, visible)

    def paintEvent(self, event: QPaintEvent):
        if self.elided:
            non_elided_text = self.non_elided_text
            self.setText(QFontMetrics(self.font()).elidedText(non_elided_text, Qt.ElideRight, self.width() - 10))
            self.non_elided_text = non_elided_text
        super().paintEvent(event)

    def init(
            self, *,
            text: str = '', alignment: Qt.Alignment = None, wrap: bool = False, size: QSize = None,
            icon: Icon = None, elided: bool = False, policy: tuple[QSizePolicy, QSizePolicy] = None
    ) -> 'Label':
        self.elided = elided
        if self.elided:
            self.non_elided_text = text
        self.setText(text)
        self.setWordWrap(wrap)
        if size:
            self.setFixedSize(size)
        if alignment:
            self.setAlignment(alignment)
        if icon:
            self.setPixmap(icon.icon.pixmap(icon.size))
        if policy:
            self.setSizePolicy(*policy)
        return self

    def setText(self, text: str) -> None:
        if self.elided:
            self.non_elided_text = text
        super().setText(text)
