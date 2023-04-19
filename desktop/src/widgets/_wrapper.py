from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QSettings
from contextlib import suppress
import uuid


class UI:
    __settings = QSettings()

    def __init__(self):
        super().__init__()

    @property
    def token(self):
        return self.__settings.value('token')

    @token.setter
    def token(self, token: str):
        self.__settings.setValue('token', token)


ui = UI()


class Wrapper:
    def __init__(self, parent: QWidget = None, name: str = str(uuid.uuid4()), visible: bool = True):
        if parent and name:
            self.setObjectName(name)
            setattr(parent, name, self)
            setattr(ui, name, self)
        with suppress(Exception):
            self.setVisible(visible)
