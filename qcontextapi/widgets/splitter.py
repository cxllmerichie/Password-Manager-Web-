from PyQt5.QtWidgets import QWidget, QSplitter
from PyQt5.QtCore import Qt
from typing import Iterable

from .widget import Widget
from .._wrapper import Wrapper


class SplitterHandle(Widget):
    def __init__(self, parent: QWidget, name: str):
        super().__init__(parent, name, True)


class Splitter(Wrapper, QSplitter):
    def __init__(self, parent: QWidget, name: str, visible: bool = True, stylesheet: str = None):
        QSplitter.__init__(self, parent)
        Wrapper.__init__(self, parent, name, visible)
        if stylesheet:
            self.setStyleSheet(stylesheet)
            self.setAttribute(Qt.WA_StyledBackground, True)

    def init(
            self, *,
            items: Iterable[QWidget] = ()
    ) -> 'Splitter':
        for item in items:
            self.addWidget(item)
        return self

    def addWidget(self, widget: QWidget) -> None:
        super().addWidget(widget)
        widget.splitter = self
