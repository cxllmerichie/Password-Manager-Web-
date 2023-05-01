from qcontextapi.widgets import Layout, Label, Selector, Frame
from PyQt5.QtWidgets import QStatusBar


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
                alignment=Layout.LeftCenter,
                items=[
                    Label(self, 'StorageLbl').init(
                        text='Storage type:'
                    ),
                    Selector(self, 'StorageSelector').init(
                        items=[
                            Selector.Item(text='local'),
                            Selector.Item(text='remote'),
                        ]
                    ), Layout.LeftBottom
                ]
            )
        ))
        return self
