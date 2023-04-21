from PyQt5.QtCore import QSettings as _QSettings
import socket as _socket


class ContextAPI:
    __settings = _QSettings(_socket.gethostname(), __file__)

    @property
    def token(self):
        return self.__settings.value('token')

    @token.setter
    def token(self, token: str):
        self.__settings.setValue('token', token)


ui = ContextAPI()
