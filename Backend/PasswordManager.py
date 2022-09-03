from argon2 import PasswordHasher
# from rsa import newkeys, encrypt, decrypt
from waitress import serve

from Frontend.app import app
from Database.Database import Database
from Logger.Logger import log, flask


class PasswordManager:
    __ph = PasswordHasher()
    # public, __private = newkeys(512)

    def __init__(self):
        self.__db = Database()
        self.__db.connect()
        self.__run()

    def __del__(self):
        self.__db.disconnect()

    @log(flask)
    def __run(self):
        serve(app, host="127.0.0.1", port=5000, threads=8)

    def __secure(self, data: str) -> str:
        # secured = self.__ph.hash(data)
        # return encrypt(secured.encode(), self.__public)
        return self.__ph.hash(data)

    def __verify(self, unsecured: str, secured: bytes) -> bool:
        # decrypted = decrypt(secured, self.__private)
        # return self.__ph.verify(unsecured, decrypted)
        return self.__ph.verify(unsecured, secured)

    def create_user(self, name: str, surname: str, username: str, password: str):
        self.__db.execute(self.__db.tables['user'].insert(
            name=name, surname=surname,
            username=self.__secure(username), password=self.__secure(password)
        ))
