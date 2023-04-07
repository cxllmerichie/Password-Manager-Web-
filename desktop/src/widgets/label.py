from PyQt5.QtGui import QFontMetrics
from PyQt5.QtWidgets import QLabel, QWidget
from PyQt5.QtCore import Qt, QSize

from ..misc import Icon, Size


class Label(QLabel):
    def __init__(self, parent: QWidget, name: str):
        super().__init__(parent)
        self.setObjectName(name)

    async def init(
            self, *,
            text: str = '', alignment: Qt.Alignment = None, wrap: bool = False, size: QSize | Size = None,
            icon: Icon = None, elided: bool = False
    ) -> 'Label':
        self.setText(text)
        self.setProperty('elided', elided)
        self.setWordWrap(wrap)
        if alignment:
            self.setAlignment(alignment)
        if size:
            if isinstance(size, QSize):
                self.setFixedSize(size)
            else:
                if size.w:
                    self.setFixedWidth(size.w)
                if size.h:
                    self.setFixedHeight(size.h)
        if icon:
            self.setPixmap(icon.icon.pixmap(icon.size))
        return self

    def paintEvent(self, event):
        if self.property('elided'):
            self.setText(QFontMetrics(self.font()).elidedText(self.text(), Qt.ElideRight, self.width() - 10))
        super().paintEvent(event)
