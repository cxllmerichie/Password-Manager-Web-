from PyQt5.QtWidgets import QStackedWidget, QWidget

from ..components.category import Category
from ..css import right_pages
from ..widgets import SideMenu


class RightPages(QStackedWidget, SideMenu):
    def __init__(self, parent: QWidget, width: int):
        super().__init__(parent)
        self.setObjectName(self.__class__.__name__)
        self.setStyleSheet(right_pages.css)

        self.expand_to = width

    async def init(self) -> 'RightPages':
        self.addWidget(await Category(self).init())
        self.shrink()
        return self
