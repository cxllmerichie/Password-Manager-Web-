from FlaskApp import app
from Database import Database
from argon2 import PasswordHasher
from rsa import newkeys, encrypt, decrypt


class PasswordManager:
    __ph = PasswordHasher()
    __public, __private = newkeys(512)

    def __init__(self):
        self.__db = Database('pypmdb.sqlite')
        self.__db.connect()

        app.run()

    def __secure(self, data: str) -> bytes:
        secured = self.__ph.hash(data)
        return encrypt(secured.encode(), self.__public)

    def __verify(self, unsecured: str, secured: bytes) -> bool:
        decrypted = decrypt(secured, self.__private)
        return self.__ph.verify(unsecured, decrypted)

    def create_user(self, name: str, surname: str, username: str, password: str):
        self.__db.execute(self.__db.tables['user'].insert(
            name=name, surname=surname,
            username=self.__secure(username), password=self.__secure(password)
        ))
