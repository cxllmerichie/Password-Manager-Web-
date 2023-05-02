from PyQt5.QtWidgets import QWidget
from time import sleep

from ..misc import ConditionalThreadQueue
from ..widgets import Label


class ErrorLabel(Label):
    def __init__(self, parent: QWidget, name: str = None, visible: bool = True):
        super().__init__(parent, name if name else self.__class__.__name__, visible)
        self.__ctq = ConditionalThreadQueue()

    def setText(self, text: str, delay: int = 3) -> None:
        if not text:  # text == '' means instantly clear the text and hide label without `post` action
            self.setVisible(False)
            return super().setText('')

        def pre():
            super().setText(text)
            self.setVisible(True)
            sleep(delay)

        def post():
            self.setText('')

        self.__ctq.new(pre, post)
