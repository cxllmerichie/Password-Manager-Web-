from dataclasses import dataclass
from PyQt5.QtCore import QSize


@dataclass()
class Size:
    w: int
    h: int


class Sizes:
    App = QSize(800, 600)
    AuthTextBtn = Size(..., 20)
    AuthMainBtn = Size(200, 30)
    AuthInputLabel = Size(..., 25)
    AuthInputField = Size(300, 25)
