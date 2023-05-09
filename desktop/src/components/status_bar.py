from qcontextapi.widgets import Layout, Label, Selector, Frame
from PyQt5.QtWidgets import QStatusBar
from PyQt5.QtCore import pyqtSlot
from qcontextapi import CONTEXT

from ..misc import utils, API


class StatusBar(QStatusBar):
    def __init__(self, parent):
        super().__init__(parent)
        self.setObjectName(self.__class__.__name__)
        # styleSheet is set in the `app.py`, where the `StatusBar` is imported, otherwise does not work

    def init(self) -> 'StatusBar':
        self.layout().setContentsMargins(5, 0, 0, 0)
        items = [self.layout().itemAt(i) for i in range(self.layout().count())]
        for item in items:
            self.layout().removeItem(item)
        self.layout().addWidget(Frame(self, 'StatusBarFrame').init(
            layout=Layout.horizontal().init(
                alignment=Layout.LeftTop,
                items=[
                    Label(self, 'StorageLbl').init(
                        text='Storage type:'
                    ),
                    Selector(self, 'StorageSelector').init(
                        textchanged=self.storage_selector_textchanged,
                        items=[
                            Selector.Item(text=utils.Storage.LOCAL.value),
                            Selector.Item(text=utils.Storage.REMOTE.value),
                        ]
                    ), Layout.LeftBottom
                ]
            )
        ))
        return self

    def post_init(self):
        self.StorageSelector.setCurrentText(CONTEXT['storage'].value)

    @pyqtSlot()
    def storage_selector_textchanged(self):
        if self.StorageSelector.currentText() == utils.Storage.LOCAL.value:
            CONTEXT['storage'] = utils.Storage.LOCAL
        else:
            CONTEXT['storage'] = utils.Storage.REMOTE
            if not CONTEXT['token']:
                return CONTEXT.CentralWidget.setCurrentWidget(CONTEXT.SignIn)
        CONTEXT.CentralWidget.setCurrentWidget(CONTEXT.MainView)
        CONTEXT.LeftMenu.refresh_categories(API.get_categories())
        CONTEXT.RightPagesCategory.show_create()
        CONTEXT.RightPages.shrink()
