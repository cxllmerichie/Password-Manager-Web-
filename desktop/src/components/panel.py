from PyQt5.QtWidgets import QWidget, QSpacerItem, QSizePolicy
from PyQt5.QtGui import QMouseEvent
from PyQt5.QtCore import Qt

from ..widgets import Button, Label, HLayout, Frame
from ..misc import Icons, Sizes
from .. import css


class Panel(QWidget):
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self.setObjectName(self.__class__.__name__)
        self.setStyleSheet(css.panel.css)
        self.setAttribute(Qt.WA_StyledBackground, True)

    def init(self) -> 'Panel':
        layout = HLayout().init(spacing=10)
        layout.addWidget(Button(self, 'ToggleLeftMenuBtn').init(
            slot=lambda: self.parent().findChild(QWidget, 'LeftMenu').toggle(), icon=Icons.MENU
        ), alignment=Qt.AlignLeft)
        layout.addWidget(Label(self, 'PanelTitleLbl').init(
            text='Password Manager'
        ), alignment=Qt.AlignLeft)
        layout.addWidget(Label(self, 'PanelTitleLbl').init(
            icon=Icons.APP
        ), alignment=Qt.AlignLeft)
        layout.addItem(QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum))

        hlayout = HLayout().init(alignment=HLayout.Right)
        hlayout.addWidget(Button(self, 'PanelMinimizeBtn').init(
            icon=Icons.MINIMIZE, size=Sizes.PanelNavigationBtn, slot=self.app().showMinimized
        ))
        hlayout.addWidget(Button(self, 'PanelRestoreBtn').init(
            icon=Icons.RESTORE, size=Sizes.PanelNavigationBtn,
            slot=lambda: self.app().showNormal() if self.app().isMaximized() else self.app().showMaximized()
        ))
        hlayout.addWidget(Button(self, 'PanelCloseBtn').init(
            icon=Icons.CROSS, size=Sizes.PanelNavigationBtn, slot=self.app().close
        ))
        layout.addWidget(Frame(self).init(layout=hlayout))
        self.setLayout(layout)
        return self

    def app(self) -> 'App':
        return self.parent().parent().parent()

    def mousePressEvent(self, event: QMouseEvent) -> None:
        self.app().setProperty('position', event.globalPos())

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        delta = event.globalPos() - self.app().property('position')
        self.app().move(self.app().x() + delta.x(), self.app().y() + delta.y())
        self.app().setProperty('position', event.globalPos())
