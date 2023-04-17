from PyQt5.QtWidgets import QWidget
from contextlib import suppress
import re
import uuid


class Wrapper:
    def __init__(self, parent: QWidget = None, name: str = str(uuid.uuid4()), visible: bool = True):
        if parent and name:
            # setattr(parent, self.__snake_case(name), self)
            setattr(parent, name, self)
            self.setObjectName(name)
        with suppress(Exception):
            self.setVisible(visible)

    @staticmethod
    def __snake_case(name: str) -> str:
        name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
        name = re.sub('([a-z0-9])([A-Z])', r'\1_\2', name)
        return name.lower()
