from dataclasses import dataclass
from PyQt5.QtCore import QSize


class Size:
    def __init__(self, width: int = ..., height: int = ...):
        self.w: int = width if width is not Ellipsis else None
        self.h: int = height if height is not Ellipsis else None


class Sizes:
    App = QSize(800, 600)
    AuthTextBtn = Size(..., 20)
    AuthMainBtn = Size(200, 30)
    AuthInputLabel = Size(..., 25)
    AuthInputField = Size(300, 25)
    NoCategoriesLbl = QSize(150, 50)
    StatusBarLbl = Size(..., 20)
    PanelNavigationBtn = QSize(30, 30)
    Panel = Size(..., 30)
