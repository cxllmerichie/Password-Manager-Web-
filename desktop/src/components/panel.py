from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout
from PyQt5.QtGui import QMouseEvent, QResizeEvent
from PyQt5.QtCore import Qt, QSize

from ..css import panel
from ..widgets import Button, Label
from ..assets import Icon


class Panel(QWidget):
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self.setObjectName(self.__class__.__name__)
        self.setStyleSheet(panel.css)
        self.setAttribute(Qt.WA_StyledBackground, True)

    async def init(self) -> 'Panel':
        self.setLayout(await self.__layout())
        return self

    async def __layout(self) -> QHBoxLayout:
        hbox = QHBoxLayout()
        hbox.addWidget(await Button(self, 'ToggleLeftMenuBtn').init(
            slot=lambda: self.parent().findChild(QWidget, 'LeftMenu').toggle(), icon=Icon.MENU
        ), alignment=Qt.AlignLeft)
        return hbox

    def resizeEvent(self, event: QResizeEvent) -> None:
        self.setFixedWidth(self.__get_app.width())

    @property
    def __get_app(self) -> 'App':
        return self.parent().parent().parent()  # App.AppPages.AppView.Panel

    def mousePressEvent(self, event: QMouseEvent) -> None:
        self.__get_app.setProperty('position', event.globalPos())

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        delta = event.globalPos() - self.__get_app.property('position')
        self.__get_app.move(self.__get_app.x() + delta.x(), self.__get_app.y() + delta.y())
        self.__get_app.setProperty('position', event.globalPos())
