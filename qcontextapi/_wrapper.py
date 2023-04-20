from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QSettings
from contextlib import suppress
import uuid
import socket


class UI:
    settings: QSettings = QSettings(socket.gethostname(), __file__)

    @property
    def token(self):
        return self.settings.value('token')

    @token.setter
    def token(self, token: str):
        self.settings.setValue('token', token)


ui = UI()


class Wrapper:
    def __init__(self, parent: QWidget = None, name: str = str(uuid.uuid4()), visible: bool = True):
        if parent and name:
            self.setObjectName(name)
            setattr(parent, name, self)
            setattr(self, parent.objectName(), parent)
            setattr(ui, name, self)

            self.core = parent
            while p := self.core.parent():
                self.core = p

        with suppress(Exception):
            self.setVisible(visible)
