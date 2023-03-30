from PyQt5.QtWidgets import QFrame, QWidget, QLayout


class Frame(QFrame):
    def __init__(self, parent: QWidget, name: str, layout: QLayout = None):
        super().__init__(parent)
        self.setObjectName(name)
        if layout:
            self.setLayout(layout)
