from PyQt5.QtCore import QSettings
import socket as _socket


class ContextApi:
    settings: QSettings = QSettings(_socket.gethostname(), __file__)

    @property
    def token(self):
        return self.settings.value('token')

    @token.setter
    def token(self, token: str):
        self.settings.setValue('token', token)


ui = ContextApi()
