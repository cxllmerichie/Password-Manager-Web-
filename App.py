from FlaskApp import app
from Database import Database


class PasswordManager:
    def __init__(self):
        self.db = Database()
        app.run()
