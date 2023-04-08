from PyQt5.QtWidgets import QFrame, QWidget, QLayout


class Frame(QFrame):
    def __init__(self, parent: QWidget, name: str = None):
        super().__init__(parent)
        if name:
            self.setObjectName(name)

    def init(
            self, *,
            layout: QLayout = None
    ) -> 'Frame':
        if layout:
            self.setLayout(layout)
        return self
